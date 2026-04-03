from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import aiohttp
import logging
from datetime import timedelta
from .const import DOMAIN
from .api import SHMUAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SHMU integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = SHMUDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator}

    # Forward setup to sensor and camera platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True
    
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, ["sensor"]):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class SHMUDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching SHMU data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the coordinator."""
        self._hass = hass
        self._entry = entry
        self._station_id = entry.data.get("station_id", "11813")
        self._meteogram_id = entry.data.get("meteogram_id", "none")
        self._verify_ssl = entry.data.get("verify_ssl", True)
        self._api = SHMUAPI(self._station_id, self._verify_ssl)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=entry.data.get("scan_interval", 300)),
        )

    async def _async_update_data(self):
        """Fetch data from SHMU API."""
        try:
            session = async_get_clientsession(self._hass)
            return await self._api.fetch_data(session)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with SHMU API: {err}")
