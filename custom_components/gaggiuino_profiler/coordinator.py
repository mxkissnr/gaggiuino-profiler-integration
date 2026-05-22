import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class GlpDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, session: aiohttp.ClientSession, url: str):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self._session = session
        self._url     = url.rstrip("/")

    async def _async_update_data(self) -> dict:
        try:
            async with self._session.get(f"{self._url}/api/status", timeout=aiohttp.ClientTimeout(total=10)) as r:
                r.raise_for_status()
                status = await r.json()

            async with self._session.get(f"{self._url}/shots.json", timeout=aiohttp.ClientTimeout(total=10)) as r:
                r.raise_for_status()
                shots = await r.json()

        except Exception as err:
            raise UpdateFailed(f"GLP unreachable: {err}") from err

        last = shots[-1] if shots else {}
        ann  = last.get("annotation") or {}

        dp       = last.get("datapoints") or {}
        pressure = dp.get("pressure") or []
        duration = dp.get("timeInShot") or []

        avg_pressure = round(sum(pressure) / len(pressure) / 10, 2) if pressure else None
        duration_s   = round(duration[-1] / 10, 1) if duration else None

        dose  = ann.get("dose")
        yield_g = None
        ratio   = None
        weight_arr = dp.get("shotWeight") or dp.get("weight") or []
        if weight_arr:
            yield_g = round(weight_arr[-1] / 10, 1)
        if dose and yield_g:
            try:
                ratio = round(float(yield_g) / float(dose), 2)
            except (ValueError, ZeroDivisionError):
                pass

        return {
            "machine_status":      "online" if not status.get("lastSyncError") else "error",
            "shot_count":          status.get("shotCount", 0),
            "last_shot_id":        last.get("id"),
            "last_shot_profile":   last.get("profileName") or last.get("profile", {}).get("name"),
            "last_shot_score":     last.get("annotation", {}).get("score") if last else None,
            "last_shot_date":      last.get("timestamp"),
            "last_shot_duration":  duration_s,
            "last_shot_pressure":  avg_pressure,
            "last_shot_weight":    yield_g,
            "last_shot_ratio":     ratio,
            "last_shot_coffee":    ann.get("coffee"),
            "last_shot_grinder":   ann.get("grinder"),
            "last_shot_dose":      float(dose) if dose else None,
            "last_sync":           status.get("lastSync"),
            "machine_url":         status.get("machineHostname"),
        }
