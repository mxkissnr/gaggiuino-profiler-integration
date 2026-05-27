"""Coordinator that polls the Gaggiuino machine live status via the GLP add-on proxy."""
import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

MACHINE_INTERVAL_SECONDS = 5


class GlpMachineCoordinator(DataUpdateCoordinator):
    """Poll /api/machine/status from the GLP add-on every 5 s.

    The add-on caches the latest /api/system/status response from the Gaggiuino
    machine so no extra machine call is needed from the integration side.
    Returns an empty dict (not an error) when the machine status is unavailable
    so entities show as unavailable rather than triggering HA error states.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        url: str,
        data_coordinator,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_machine",
            update_interval=timedelta(seconds=MACHINE_INTERVAL_SECONDS),
        )
        self._session          = session
        self._url              = url.rstrip("/")
        self._data_coordinator = data_coordinator

    async def _async_update_data(self) -> dict:
        try:
            async with self._session.get(
                f"{self._url}/api/machine/status",
                headers=self._data_coordinator._headers,
                timeout=aiohttp.ClientTimeout(total=5),
            ) as r:
                r.raise_for_status()
                data = await r.json()
                # available=false → return empty dict, entities become unavailable
                if not data.get("available"):
                    return {}
                return data
        except Exception as err:
            raise UpdateFailed(f"GLP machine status unreachable: {err}") from err
