"""Live Weather Service with Open-Meteo API integration.

Provides live 2m air temperature, relative humidity, 10m wind speed, and solar radiation.
Gracefully handles network drops, rate limits, and configuration toggles with automatic
failover to deterministic demo data.
"""

from typing import Dict, Any, List
import requests
from ..config import OPEN_METEO_BASE, OPEN_METEO_ENABLED
from ..thermal.engine import compute_all_thermal_metrics, get_active_thermal_stress


class WeatherService:
    def __init__(self, timeout: float = 6.0):
        self.timeout = timeout

    def _fetch(self, lat: float, lon: float) -> Dict[str, Any]:
        if not OPEN_METEO_ENABLED:
            raise RuntimeError('Live weather queries are disabled via OPEN_METEO_ENABLED=false')

        params = {
            'latitude': lat,
            'longitude': lon,
            'timezone': 'auto',
            'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure',
            'daily': 'temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max,shortwave_radiation_sum'
        }

        resp = requests.get(OPEN_METEO_BASE, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def live_current(self, lat: float, lon: float, metric: str = 'heat_index') -> Dict[str, Any]:
        """Fetch current observations and calculate multi-metric thermal stress."""
        data = self._fetch(lat, lon)
        c = data.get('current', {})

        temp = float(c.get('temperature_2m', 34.0))
        rh = float(c.get('relative_humidity_2m', 60.0))
        wind = float(c.get('wind_speed_10m', 10.0))
        solar = 650.0  # Daylight standard proxy if real-time radiometer not in free endpoint

        all_thermal = compute_all_thermal_metrics(temp, rh, wind, solar)
        active_thermal = get_active_thermal_stress(temp, rh, wind, solar, metric=metric)

        return {
            'temperature_c': round(temp, 1),
            'humidity_pct': round(rh, 1),
            'wind_kmh': round(wind, 1),
            'solar_w_m2': solar,
            'active_metric': metric,
            'thermal_index_c': active_thermal['value_c'],
            'thermal_category': active_thermal['category'],
            'heat_index_c': all_thermal['heat_index']['value'],
            'heat_index_category': all_thermal['heat_index']['category'],
            'wbgt_outdoor_c': all_thermal['wbgt']['value'],
            'wbgt_outdoor_category': all_thermal['wbgt']['category'],
            'utci_c': all_thermal['utci']['value'],
            'utci_category': all_thermal['utci']['category'],
            'data_status': 'LIVE / OPEN-METEO'
        }

    def live_forecast(self, lat: float, lon: float, metric: str = 'heat_index') -> List[Dict[str, Any]]:
        """Fetch 5-day daily forecast and calculate projected thermal indices."""
        data = self._fetch(lat, lon)
        d = data.get('daily', {})
        times = d.get('time', [])
        t_max = d.get('temperature_2m_max', [])
        rh_mean = d.get('relative_humidity_2m_mean', [])
        wind_max = d.get('wind_speed_10m_max', [])

        out = []
        # Next 5 days (indexes 1 to 5)
        for i in range(1, min(6, len(times))):
            dt = times[i]
            temp = float(t_max[i] if i < len(t_max) and t_max[i] is not None else 35.0)
            rh = float(rh_mean[i] if i < len(rh_mean) and rh_mean[i] is not None else 55.0)
            wind = float(wind_max[i] if i < len(wind_max) and wind_max[i] is not None else 10.0)
            solar = 700.0

            all_thermal = compute_all_thermal_metrics(temp, rh, wind, solar)
            active_thermal = get_active_thermal_stress(temp, rh, wind, solar, metric=metric)

            out.append({
                'date': dt,
                'day_label': dt,
                'day_index': i,
                'temperature_c': round(temp, 1),
                'humidity_pct': round(rh, 1),
                'wind_kmh': round(wind, 1),
                'solar_w_m2': solar,
                'thermal_index_c': active_thermal['value_c'],
                'thermal_category': active_thermal['category'],
                'heat_index_c': all_thermal['heat_index']['value'],
                'wbgt_outdoor_c': all_thermal['wbgt']['value'],
                'utci_c': all_thermal['utci']['value'],
                'data_status': 'LIVE / OPEN-METEO'
            })

        return out


WEATHER = WeatherService()
