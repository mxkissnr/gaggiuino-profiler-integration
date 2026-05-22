import logging
from datetime import datetime, timedelta, timezone

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


def _parse_ts(value: object) -> datetime | None:
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            # Unix ms timestamp
            return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
        s = str(value)
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


class GlpDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, session: aiohttp.ClientSession, url: str, scan_interval: int = SCAN_INTERVAL_SECONDS):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self._session = session
        self._url     = url.rstrip("/")
        self._last_shot_id: int | None = None

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

        current_shot_id = last.get("id")

        data = {
            "machine_status":      "online" if not status.get("lastSyncError") else "error",
            "shot_count":          status.get("shotCount", 0),
            "last_shot_id":        current_shot_id,
            "last_shot_profile":   last.get("profileName") or last.get("profile", {}).get("name"),
            "last_shot_score":     last.get("annotation", {}).get("score") if last else None,
            "last_shot_date":      _parse_ts(last.get("timestamp")),
            "last_shot_duration":  duration_s,
            "last_shot_pressure":  avg_pressure,
            "last_shot_weight":    yield_g,
            "last_shot_ratio":     ratio,
            "last_shot_coffee":    ann.get("coffee"),
            "last_shot_grinder":   ann.get("grinder"),
            "last_shot_dose":      float(dose) if dose else None,
            "last_sync":           _parse_ts(status.get("lastSync")),
            "machine_url":         status.get("machineHostname"),
        }

        if current_shot_id and current_shot_id != self._last_shot_id and self._last_shot_id is not None:
            self.hass.bus.async_fire(
                f"{DOMAIN}_shot_completed",
                {
                    "shot_id":      current_shot_id,
                    "profile":      data["last_shot_profile"],
                    "duration_s":   data["last_shot_duration"],
                    "yield_g":      data["last_shot_weight"],
                    "dose_g":       data["last_shot_dose"],
                    "ratio":        data["last_shot_ratio"],
                    "avg_pressure": data["last_shot_pressure"],
                    "score":        data["last_shot_score"],
                    "coffee":       data["last_shot_coffee"],
                    "grinder":      data["last_shot_grinder"],
                },
            )

        self._last_shot_id = current_shot_id
        return data
