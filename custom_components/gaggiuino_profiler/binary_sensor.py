from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GlpDataCoordinator
from .live_coordinator import GlpLiveCoordinator
from .machine_coordinator import GlpMachineCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    live_coordinator: GlpLiveCoordinator       = hass.data[DOMAIN][entry.entry_id]["live"]
    data_coordinator: GlpDataCoordinator       = hass.data[DOMAIN][entry.entry_id]["data"]
    machine_coordinator: GlpMachineCoordinator = hass.data[DOMAIN][entry.entry_id]["machine"]
    async_add_entities([
        IsBrewingSensor(live_coordinator, entry),
        PreheatReadySensor(data_coordinator, entry),
        SteamSwitchSensor(machine_coordinator, entry),
    ])


class IsBrewingSensor(CoordinatorEntity[GlpLiveCoordinator], BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Brewing"
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = "mdi:coffee-maker-check-outline"

    def __init__(self, coordinator: GlpLiveCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_is_brewing"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gaggiuino Local Profiler",
            manufacturer="Gaggiuino",
            model="Local Profiler",
            configuration_url=entry.data["url"],
        )

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return bool(self.coordinator.data.get("isLive"))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data
        if not data:
            return {}
        dp = data.get("datapoints")
        if not dp:
            return {}
        return {
            "profile_name": data.get("profileName"),
            "seq":          data.get("seq"),
            "datapoints":   dp,
        }


class PreheatReadySensor(CoordinatorEntity[GlpDataCoordinator], BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Preheat Ready"
    _attr_icon = "mdi:coffee-maker-check"

    def __init__(self, coordinator: GlpDataCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_preheat_ready"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gaggiuino Local Profiler",
            manufacturer="Gaggiuino",
            model="Local Profiler",
            configuration_url=entry.data["url"],
        )

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return bool(self.coordinator.data.get("preheat_ready"))


class SteamSwitchSensor(CoordinatorEntity[GlpMachineCoordinator], BinarySensorEntity):
    """Physical steam switch state from the Gaggiuino machine."""

    _attr_has_entity_name = True
    _attr_name = "Steam Switch"
    _attr_device_class = BinarySensorDeviceClass.HEAT
    _attr_icon = "mdi:weather-fog"

    def __init__(self, coordinator: GlpMachineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_steam_switch"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gaggiuino Local Profiler",
            manufacturer="Gaggiuino",
            model="Local Profiler",
            configuration_url=entry.data["url"],
        )

    @property
    def available(self) -> bool:
        return bool(self.coordinator.data)

    @property
    def is_on(self) -> bool | None:
        if not self.coordinator.data:
            return None
        return bool(self.coordinator.data.get("steamSwitchState"))
