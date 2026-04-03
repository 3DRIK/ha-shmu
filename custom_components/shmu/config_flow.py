from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
from .const import DOMAIN

class SHMUConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SHMU."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"SHMU Station {user_input['station_id']}",
                data={
                    "station_id": user_input["station_id"],
                    "meteogram_id": user_input["meteogram_id"],
                    "scan_interval": user_input["scan_interval"],
                    "verify_ssl": user_input["verify_ssl"],
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("station_id", default="11813"): str,
                    vol.Optional("meteogram_id", default="32737"): str,
                    vol.Optional("scan_interval", default=300): int,
                    vol.Optional("verify_ssl", default=True): bool,
                }
            ),
            errors=errors,
        )
