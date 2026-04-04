# ha-shmu
# SHMU Integration for Home Assistant

This integration fetches meteorological data from the [Slovenský hydrometeorologický ústav (SHMU)](https://www.shmu.sk/) and provides sensors for temperature, humidity, pressure, wind speed, and wind direction. It also generates a meteogram image URL.
This is only integration, all data is provided by [SHMU Open Data](https://opendata.shmu.sk/).

## Installation

1. **Add this repository to HACS**:
   - Go to HACS > Integrations > Custom Repositories.
   - Add `https://github.com/3DRIK/ha-shmu` as a custom repository.
   - Install the "SHMU" integration.

2. **Configure the integration**:
   - Go to Configuration > Integrations > Add Integration > SHMU.
   - Tap `Add hub` to enter cobfiguration flow (you can add multiple stations)

## Configuration Options

| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| Station ID     | ID of the SHMU meteorological station (e.g., `11813` for Bratislava).      |
| Meteogram ID   | ID of the SHMU meteogram loaction (e.g., `32737` for Bratislava or `none` for no meteogram). |
| Scan Interval  | How often (in seconds) the data should be updated (default: 300 seconds).  |
| Verify SSL     | Verifying SHMU API SSL (recommended).                                      |

- You can find your nearest station at [SHMU Stations](https://www.shmu.sk/sk//?page=1&id=meteo_apocasie_sk) with ID in URL.
- You can find Meteogram locations at [SHMU Meteograms](https://www.shmu.sk/sk/?page=769) with ID in URL.

## Sensors

The integration creates device with the following sensors:

- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- Wind Speed (m/s)
- Wind Direction (°)
- Global radiation (W/m²)
- Sun duration/min (s)
- Precipitation volume/min (mm)
- Precipitation duration/min (s)
- Meteogram url (containing meteogram image url for 3 and 10 days in attributes)

## Meteogram

The integration provides URL for camera entity for the meteogram image, which updates automatically based on the current time. URL is available as a sensor atribute.

Add to generic camera as static image:
`{{state_attr('sensor.shmu_meteogram_url', 'meteogram_3d_url') }}`
or for 10d meteogram:
`{{state_attr('sensor.shmu_meteogram_url', 'meteogram_10d_url') }}`

## Troubleshooting

- Ensure your station ID is correct.
- Check the logs for errors if sensors are unavailable.
- For some stations, data or some attributes are not available.
- Sometimes there may be a delay in the publication of data or a longer period with no data published.
