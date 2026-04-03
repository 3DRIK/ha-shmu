# ha-shmu2
# SHMU Integration for Home Assistant

This integration fetches meteorological data from the [Slovenský hydrometeorologický ústav (SHMU)](https://www.shmu.sk/) and provides sensors for temperature, humidity, pressure, wind speed, and wind direction. It also generates a meteogram image URL.

## Installation

1. **Add this repository to HACS**:
   - Go to HACS > Integrations > Custom Repositories.
   - Add `https://github.com/yourusername/shmu-integration` as a custom repository.
   - Install the "SHMU" integration.

2. **Configure the integration**:
   - Go to Configuration > Integrations > Add Integration > SHMU.
   - Enter your station ID (e.g., `11813` for Bratislava) and scan interval.

## Configuration Options

| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| Station ID     | ID of the SHMU meteorological station (e.g., `11813` for Bratislava).      |
| Scan Interval  | How often (in seconds) the data should be updated (default: 300 seconds).  |

## Sensors

The integration creates the following sensors:

- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- Wind Speed (m/s)
- Wind Direction (°)

## Meteogram

The integration provides URL for camera entity for the meteogram image, which updates automatically based on the current time.

Add to generic camera using
`{{state_attr('sensor.shmu_meteogram_url', 'meteogram_url') }}`

## Troubleshooting

- Ensure your station ID is correct.
- Check the logs for errors if sensors are unavailable.
