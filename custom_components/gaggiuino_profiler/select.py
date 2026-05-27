"""Profile selector for the Gaggiuino machine — replaces ALERTua/hass-gaggiuino."""
from __future__ import annotations

import logging

import aiohttp
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GlpDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GlpDataCoordinator = hass.data[DOMAIN][entry.entry_id]["data"]
    async_add_entities([GlpProfileSelect(coordinator, entry)])


class GlpProfileSelect(CoordinatorEntity[GlpDataCoordinator], SelectEntity):
    """Gaggiuino brew profile selector.

    Reads available profiles and the current selection from the GLP add-on
    (/api/machine/profiles), which in turn calls the Gaggiuino machine directly.
    Writing a new profile calls /api/machine/profile/set on the add-on.
    """

    _attr_has_entity_name = True
    _attr_name = "Profile"
    _attr_icon = "mdi:coffee"

    def __init__(self, coordinator: GlpDataCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_profile"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gaggiuino Local Profiler",
            manufacturer="Gaggiuino",
            model="Local Profiler",
            configuration_url=entry.data["url"],
        )
        self._url = entry.data["url"].rstrip("/")

    @property
    def options(self) -> list[str]:
        return self.coordinator.data.get("profile_options") or []

    @property
    def current_option(self) -> str | None:
        return self.coordinator.data.get("current_profile")

    @property
    def available(self) -> bool:
        return bool(self.options)

    async def async_select_option(self, option: str) -> None:
        session = async_get_clientsession(self.hass)
        try:
            async with session.post(
                f"{self._url}/api/machine/profile/set",
                json={"option": option},
                headers=self.coordinator._headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                r.raise_for_status()
        except Exception as err:
            _LOGGER.error("Failed to set profile %s: %s", option, err)
            raise
        # Trigger immediate refresh so the UI reflects the new selection
        await self.coordinator.async_request_refresh()
