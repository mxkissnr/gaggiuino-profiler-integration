from __future__ import annotations

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_URL, DOMAIN


class GlpConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            url = user_input["url"].rstrip("/")
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(
                    f"{url}/api/status",
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    r.raise_for_status()
            except Exception:
                errors["url"] = "cannot_connect"
            else:
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=url.removeprefix("http://").removeprefix("https://"),
                    data={"url": url},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("url", default=DEFAULT_URL): str}
            ),
            errors=errors,
        )
