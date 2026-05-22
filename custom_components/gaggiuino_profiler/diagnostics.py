from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import GlpDataCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    coordinator: GlpDataCoordinator = hass.data[DOMAIN][entry.entry_id]["data"]
    return {
        "config_entry": {"url": entry.data.get("url"), "options": dict(entry.options)},
        "coordinator_data": {
            k: str(v) if hasattr(v, "isoformat") else v
            for k, v in (coordinator.data or {}).items()
            if k != "last_shot_id"
        },
    }
