import aiohttp
import async_timeout
import logging
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

class SHMUAPI:
    """Class to handle SHMU API communication."""

    def __init__(self, station_id: str, verify_ssl: bool = True):
        """Initialize the API client."""
        self._station_id = station_id
        self._verify_ssl = verify_ssl

    def _generate_url(self):
        """Generate the dynamic URL for SHMU data."""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1) #there is delay <1 min in shmu file publish time
        date_str = one_minute_ago.strftime("%Y%m%d")
        time_str = f"{one_minute_ago.strftime('%H')}-{'%02d' % ((one_minute_ago.minute // 5) * 5)}-00"
        return (
            f"https://opendata.shmu.sk/meteorology/climate/now/data/"
            f"{date_str}/aws1min%20-%20{one_minute_ago.strftime('%Y-%m-%d')} {time_str}.json"
        )

    async def fetch_data(self, session: aiohttp.ClientSession):
        """Fetch data from SHMU API."""
        url = self._generate_url()
        _LOGGER.debug("Fetching SHMU data from URL: %s", url)

        try:
            ssl_context = None
            if not self._verify_ssl:
                connector = aiohttp.TCPConnector(ssl=False)
            else:
                connector = aiohttp.TCPConnector()

            async with aiohttp.ClientSession(connector=connector) as api_session:
                async with async_timeout.timeout(10):
                    async with api_session.get(url) as response:
                        if response.status != 200:
                            raise Exception(f"Error fetching SHMU data: HTTP {response.status} for URL: {url}")
                        data = await response.json()
                        station_data = [
                            item for item in data.get("data", [])
                            if str(item.get("ind_kli")) == self._station_id
                        ]
                        if not station_data:
                            raise Exception(f"No data found for station ID: {self._station_id}")
                        return station_data[0]
        except aiohttp.ClientError as err:
            raise Exception(f"Communication error with SHMU API: {err}")
        except Exception as err:
            raise Exception(f"Unexpected error: {err}")
