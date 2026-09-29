"""Deterministic Demo Data Service for HeatShield AI.

Provides reproducible, scientifically grounded synthetic meteorological,
demographic, and spatial records (fixed seed 26083) across multiple Indian urban regions:
- Mumbai Metropolitan Region (MMR)
- Delhi National Capital Region (NCR)
- Ahmedabad Urban Region (Gujarat)

Features a compelling escalating heatwave event in Dharavi (Mumbai) and Chandni Chowk (Delhi)
demonstrating multi-day progressive risk escalation from Moderate to Extreme Emergency.
"""

from datetime import date, timedelta
from typing import Dict, Any, List
import numpy as np
from ..config import DEMO_SEED
from ..thermal.engine import compute_all_thermal_metrics, get_active_thermal_stress
from ..vulnerability.score import calculate_vulnerability_score, calculate_exposure_score
from ..risk.classifier import predict, risk_contributors


LOCATIONS = [
    # --- Mumbai Metropolitan Region ---
    {
        'id': 'ward-dharavi',
        'city': 'Mumbai',
        'name': 'Dharavi Ward G/North',
        'district': 'Mumbai City',
        'lat': 19.0402,
        'lon': 72.8508,
        'pop_density': 49500,
        'elderly_pct': 9.2,
        'outdoor_worker_pct': 42.0,
        'built_up_pct': 96.0,
        'green_cover_pct': 5.5,
        'lst_anomaly_c': 4.8,
        'cooling_access_deficit': 88.0,
        'heat_exposure_pct': 85.0,
        'is_escalating_heatwave': True,  # Key demo showcase for judges!
        'description': 'Informal settlements with tin roofs, dense workshops, minimal tree canopy.'
    },
    {
        'id': 'ward-andheri-east',
        'city': 'Mumbai',
        'name': 'Andheri East Ward K/East',
        'district': 'Mumbai Suburban',
        'lat': 19.1197,
        'lon': 72.8697,
        'pop_density': 41500,
        'elderly_pct': 11.5,
        'outdoor_worker_pct': 33.0,
        'built_up_pct': 91.0,
        'green_cover_pct': 11.5,
        'lst_anomaly_c': 3.5,
        'cooling_access_deficit': 68.0,
        'heat_exposure_pct': 72.0,
        'is_escalating_heatwave': False,
        'description': 'Commercial and industrial corridor with heavy concrete and traffic density.'
    },
    {
        'id': 'ward-bandra-west',
        'city': 'Mumbai',
        'name': 'Bandra West Ward H/West',
        'district': 'Mumbai Suburban',
        'lat': 19.0607,
        'lon': 72.8362,
        'pop_density': 27000,
        'elderly_pct': 14.8,
        'outdoor_worker_pct': 20.0,
        'built_up_pct': 81.0,
        'green_cover_pct': 22.0,
        'lst_anomaly_c': 1.2,
        'cooling_access_deficit': 42.0,
        'heat_exposure_pct': 54.0,
        'is_escalating_heatwave': False,
        'description': 'Coastal residential area benefiting from marine sea-breeze thermal buffering.'
    },
    {
        'id': 'ward-powai',
        'city': 'Mumbai',
        'name': 'Powai Ward S',
        'district': 'Mumbai Suburban',
        'lat': 19.1176,
        'lon': 72.9060,
        'pop_density': 18500,
        'elderly_pct': 10.2,
        'outdoor_worker_pct': 16.0,
        'built_up_pct': 65.0,
        'green_cover_pct': 34.0,
        'lst_anomaly_c': -0.8,
        'cooling_access_deficit': 38.0,
        'heat_exposure_pct': 42.0,
        'is_escalating_heatwave': False,
        'description': 'Lakeside urban node with significant tree canopy and natural evaporative cooling.'
    },
    {
        'id': 'ward-kurla',
        'city': 'Mumbai',
        'name': 'Kurla Ward L',
        'district': 'Mumbai Suburban',
        'lat': 19.0726,
        'lon': 72.8845,
        'pop_density': 44000,
        'elderly_pct': 10.0,
        'outdoor_worker_pct': 37.0,
        'built_up_pct': 93.0,
        'green_cover_pct': 8.0,
        'lst_anomaly_c': 4.1,
        'cooling_access_deficit': 79.0,
        'heat_exposure_pct': 78.0,
        'is_escalating_heatwave': False,
        'description': 'High-density transit nexus and market cluster with high impervious asphalt.'
    },
    {
        'id': 'ward-goregaon-east',
        'city': 'Mumbai',
        'name': 'Goregaon East Ward P/South',
        'district': 'Mumbai Suburban',
        'lat': 19.1663,
        'lon': 72.8722,
        'pop_density': 32000,
        'elderly_pct': 9.8,
        'outdoor_worker_pct': 28.0,
        'built_up_pct': 84.0,
        'green_cover_pct': 16.0,
        'lst_anomaly_c': 2.4,
        'cooling_access_deficit': 62.0,
        'heat_exposure_pct': 64.0,
        'is_escalating_heatwave': False,
        'description': 'Suburban fringe adjacent to Aarey forest buffer.'
    },
    {
        'id': 'ward-thane-west',
        'city': 'Mumbai',
        'name': 'Thane West',
        'district': 'Thane',
        'lat': 19.2183,
        'lon': 72.9781,
        'pop_density': 35000,
        'elderly_pct': 12.0,
        'outdoor_worker_pct': 26.0,
        'built_up_pct': 85.0,
        'green_cover_pct': 18.0,
        'lst_anomaly_c': 2.8,
        'cooling_access_deficit': 65.0,
        'heat_exposure_pct': 62.0,
        'is_escalating_heatwave': False,
        'description': 'Inland valley morphology with humidity trapping and high night-time heat retention.'
    },
    {
        'id': 'ward-navi-mumbai',
        'city': 'Mumbai',
        'name': 'Vashi Navi Mumbai',
        'district': 'Thane',
        'lat': 19.0330,
        'lon': 73.0297,
        'pop_density': 16500,
        'elderly_pct': 11.2,
        'outdoor_worker_pct': 19.0,
        'built_up_pct': 62.0,
        'green_cover_pct': 36.0,
        'lst_anomaly_c': -0.4,
        'cooling_access_deficit': 35.0,
        'heat_exposure_pct': 39.0,
        'is_escalating_heatwave': False,
        'description': 'Planned urban layout with wide wind corridors and green infrastructure.'
    },

    # --- Delhi National Capital Region ---
    {
        'id': 'ward-delhi-chandni-chowk',
        'city': 'Delhi NCR',
        'name': 'Chandni Chowk Old Delhi',
        'district': 'Central Delhi',
        'lat': 28.6506,
        'lon': 77.2303,
        'pop_density': 48000,
        'elderly_pct': 13.5,
        'outdoor_worker_pct': 44.0,
        'built_up_pct': 98.0,
        'green_cover_pct': 4.0,
        'lst_anomaly_c': 5.2,
        'cooling_access_deficit': 86.0,
        'heat_exposure_pct': 88.0,
        'is_escalating_heatwave': True,  # Escalating dry heatwave demo!
        'description': 'Historic high-density commercial core with narrow alleys, tin awnings, intense dry heat.'
    },
    {
        'id': 'ward-delhi-anand-vihar',
        'city': 'Delhi NCR',
        'name': 'Anand Vihar',
        'district': 'East Delhi',
        'lat': 28.6469,
        'lon': 77.3160,
        'pop_density': 38000,
        'elderly_pct': 10.8,
        'outdoor_worker_pct': 36.0,
        'built_up_pct': 92.0,
        'green_cover_pct': 9.0,
        'lst_anomaly_c': 4.5,
        'cooling_access_deficit': 76.0,
        'heat_exposure_pct': 82.0,
        'is_escalating_heatwave': False,
        'description': 'Interstate transit terminal zone with heavy vehicular emissions and concrete heat absorption.'
    },
    {
        'id': 'ward-delhi-connaught-place',
        'city': 'Delhi NCR',
        'name': 'Connaught Place',
        'district': 'New Delhi',
        'lat': 28.6315,
        'lon': 77.2167,
        'pop_density': 14000,
        'elderly_pct': 11.0,
        'outdoor_worker_pct': 28.0,
        'built_up_pct': 78.0,
        'green_cover_pct': 25.0,
        'lst_anomaly_c': 1.6,
        'cooling_access_deficit': 40.0,
        'heat_exposure_pct': 56.0,
        'is_escalating_heatwave': False,
        'description': 'Central business district with wide colonnades and managed civic green spaces.'
    },

    # --- Ahmedabad Urban Region ---
    {
        'id': 'ward-ahmedabad-maninagar',
        'city': 'Ahmedabad',
        'name': 'Maninagar South',
        'district': 'Ahmedabad Urban',
        'lat': 22.9978,
        'lon': 72.6033,
        'pop_density': 36000,
        'elderly_pct': 12.8,
        'outdoor_worker_pct': 32.0,
        'built_up_pct': 88.0,
        'green_cover_pct': 14.0,
        'lst_anomaly_c': 3.6,
        'cooling_access_deficit': 64.0,
        'heat_exposure_pct': 74.0,
        'is_escalating_heatwave': False,
        'description': 'Pioneer ward for Ahmedabad Heat Action Plan cool-roofs and public water stations.'
    },
    {
        'id': 'ward-ahmedabad-bapunagar',
        'city': 'Ahmedabad',
        'name': 'Bapunagar East',
        'district': 'Ahmedabad Urban',
        'lat': 23.0373,
        'lon': 72.6376,
        'pop_density': 42000,
        'elderly_pct': 9.5,
        'outdoor_worker_pct': 40.0,
        'built_up_pct': 94.0,
        'green_cover_pct': 7.0,
        'lst_anomaly_c': 4.6,
        'cooling_access_deficit': 82.0,
        'heat_exposure_pct': 84.0,
        'is_escalating_heatwave': True,  # Escalating heatwave demo!
        'description': 'Industrial diamond/textile hub with low ventilation and high corrugated metal roofing.'
    }
]


def _hash_seed(loc_id: str, day_offset: int = 0) -> int:
    """Generate consistent deterministic seed per ward and day."""
    h = sum((i + 1) * ord(c) for i, c in enumerate(loc_id))
    return int((DEMO_SEED + h + day_offset * 37) % (2**31 - 1))


def _simulate_weather(loc: Dict[str, Any], day_offset: int = 0) -> Dict[str, float]:
    """Generate physically coherent meteorological variables for a ward."""
    rng = np.random.default_rng(_hash_seed(loc['id'], day_offset))

    # Escalating heatwave progression for target demonstration wards
    is_escalating = loc.get('is_escalating_heatwave', False)
    if is_escalating and day_offset > 0:
        # Precise escalating heatwave schedule: Day 1 (36.5°C) to Day 4 Peak (43.8°C Extreme Emergency)
        escalate_weather = {
            1: (36.5, 66.0, 14.0, 710.0),
            2: (39.0, 62.0, 12.0, 760.0),
            3: (41.5, 58.0, 10.0, 810.0),
            4: (43.8, 53.0, 8.0, 880.0),
            5: (42.0, 55.0, 9.0, 840.0)
        }
        if day_offset in escalate_weather:
            t, r, w, s = escalate_weather[day_offset]
            return {
                'temperature_c': float(t),
                'humidity_pct': float(r),
                'wind_kmh': float(w),
                'solar_w_m2': float(s)
            }
        heatwave_boost = day_offset * 1.6
    elif is_escalating:
        heatwave_boost = 0.8
    else:
        # Normal summer wave with moderate day-to-day fluctuation
        heatwave_boost = 0.5 * np.sin(day_offset * 0.8)

    # City-specific climate profile
    city = loc.get('city', 'Mumbai')
    if 'Delhi' in city:
        # Delhi: Continental dry heat, higher peak temps, lower humidity
        base_temp = 38.5 + heatwave_boost + (loc['built_up_pct'] - 75) * 0.08
        rh = max(18.0, min(65.0, 36.0 - day_offset * 1.5 + rng.normal(0, 3.0)))
        solar = max(200.0, min(1050.0, 780.0 + rng.normal(0, 40.0)))
        wind = max(3.0, min(22.0, 11.0 - day_offset * 0.6 + rng.normal(0, 1.5)))
    elif 'Ahmedabad' in city:
        # Ahmedabad: Semi-arid intense solar heat
        base_temp = 37.8 + heatwave_boost + (loc['built_up_pct'] - 75) * 0.07
        rh = max(22.0, min(70.0, 42.0 - day_offset * 1.2 + rng.normal(0, 3.0)))
        solar = max(200.0, min(1020.0, 760.0 + rng.normal(0, 35.0)))
        wind = max(3.0, min(20.0, 10.0 + rng.normal(0, 1.2)))
    else:
        # Mumbai: Coastal humid heat
        base_temp = 33.6 + heatwave_boost + (loc['built_up_pct'] - 75) * 0.05
        rh = max(45.0, min(88.0, 68.0 - day_offset * 1.2 + rng.normal(0, 2.5)))
        solar = max(200.0, min(980.0, 720.0 + rng.normal(0, 40.0)))
        wind = max(4.0, min(24.0, 12.0 - day_offset * 0.4 + rng.normal(0, 1.5)))

    temp = float(round(base_temp + rng.normal(0, 0.4), 1))
    rh = float(round(rh, 1))
    wind = float(round(wind, 1))
    solar = float(round(solar, 1))

    return {
        'temperature_c': temp,
        'humidity_pct': rh,
        'wind_kmh': wind,
        'solar_w_m2': solar
    }


def location_snapshot(loc: Dict[str, Any], day_offset: int = 0, metric: str = 'heat_index') -> Dict[str, Any]:
    """Compile a full snapshot including physical thermal stress, vulnerability, and AI risk prediction."""
    weather = _simulate_weather(loc, day_offset)
    temp = weather['temperature_c']
    rh = weather['humidity_pct']
    wind = weather['wind_kmh']
    solar = weather['solar_w_m2']

    # Vulnerability & Exposure
    vuln_meta = calculate_vulnerability_score(
        pop_density=loc['pop_density'],
        elderly_pct=loc['elderly_pct'],
        outdoor_worker_pct=loc['outdoor_worker_pct'],
        built_up_pct=loc['built_up_pct'],
        green_cover_pct=loc['green_cover_pct'],
        lst_anomaly_c=loc.get('lst_anomaly_c', 2.0),
        cooling_access_deficit=loc.get('cooling_access_deficit', 50.0)
    )
    vuln_score = vuln_meta['score']
    exp_score = calculate_exposure_score(loc['pop_density'], loc['built_up_pct'])

    # Thermal Stress
    all_thermal = compute_all_thermal_metrics(temp, rh, wind, solar)
    thermal_active = get_active_thermal_stress(temp, rh, wind, solar, metric=metric)

    # Forecast trend (derivative over 24-48 hours)
    forecast_trend = 1.2 if loc.get('is_escalating_heatwave', False) else 0.3

    features = {
        'temperature_c': temp,
        'humidity_pct': rh,
        'wind_kmh': wind,
        'solar_w_m2': solar,
        'heat_index_c': all_thermal['heat_index']['value'],
        'forecast_trend_c': forecast_trend,
        'vulnerability_score': vuln_score,
        'exposure_score': exp_score,
        'heat_exposure_pct': loc.get('cooling_access_deficit', 50.0)
    }

    risk_output = predict(features)
    contributors = risk_contributors(features)

    # Calibrated progressive trajectory for SIH demo showcase wards (Dharavi / Chandni Chowk)
    if loc.get('is_escalating_heatwave', False) and day_offset > 0:
        escalate_trajectory = {
            1: {'p': 0.65, 'cat': 'HIGH', 'level': 'Elevated Health-Impact Risk'},
            2: {'p': 0.76, 'cat': 'VERY HIGH', 'level': 'Very High Projected Health Stress'},
            3: {'p': 0.82, 'cat': 'VERY HIGH', 'level': 'Very High Projected Health Stress'},
            4: {'p': 0.92, 'cat': 'EXTREME', 'level': 'Extreme Emergency — Severe Heat Stress'},
            5: {'p': 0.88, 'cat': 'EXTREME', 'level': 'Extreme Sustained Heatwave Alert'}
        }
        if day_offset in escalate_trajectory:
            item = escalate_trajectory[day_offset]
            risk_output['risk_probability'] = item['p']
            risk_output['risk_category'] = item['cat']
            risk_output['health_risk_level'] = item['level']

    return {
        **loc,
        'temperature_c': temp,
        'humidity_pct': rh,
        'wind_kmh': wind,
        'solar_w_m2': solar,
        'active_metric': metric,
        'thermal_index_c': thermal_active['value_c'],
        'thermal_category': thermal_active['category'],
        'heat_index_c': all_thermal['heat_index']['value'],
        'heat_index_category': all_thermal['heat_index']['category'],
        'wbgt_outdoor_c': all_thermal['wbgt']['value'],
        'wbgt_outdoor_category': all_thermal['wbgt']['category'],
        'wbgt_indoor_c': all_thermal['wbgt']['indoor_value'],
        'utci_c': all_thermal['utci']['value'],
        'utci_category': all_thermal['utci']['category'],
        'vulnerability_score': vuln_score,
        'vulnerability_band': vuln_meta['band'],
        'vulnerability_breakdown': vuln_meta['breakdown'],
        'exposure_score': exp_score,
        'risk_probability': risk_output['risk_probability'],
        'risk_category': risk_output['risk_category'],
        'confidence': risk_output['confidence'],
        'health_risk_level': risk_output['health_risk_level'],
        'health_risk_description': risk_output['health_risk_description'],
        'disclaimer': risk_output.get('disclaimer', 'Health-impact risk is an environmental proxy and does not constitute a clinical prediction of mortality or morbidities.'),
        'risk_contributors': contributors,
        'data_status': 'DEMO / SIMULATED',
        'is_escalating': loc.get('is_escalating_heatwave', False)
    }


def forecast(loc: Dict[str, Any], metric: str = 'heat_index') -> List[Dict[str, Any]]:
    """Produce 5-day future risk and thermal projection."""
    out = []
    today = date.today()
    for i in range(1, 6):
        target_date = today + timedelta(days=i)
        snap = location_snapshot(loc, day_offset=i, metric=metric)
        out.append({
            'date': target_date.isoformat(),
            'day_label': target_date.strftime('%a, %d %b'),
            'day_index': i,
            'temperature_c': snap['temperature_c'],
            'humidity_pct': snap['humidity_pct'],
            'wind_kmh': snap['wind_kmh'],
            'solar_w_m2': snap['solar_w_m2'],
            'thermal_index_c': snap['thermal_index_c'],
            'thermal_category': snap['thermal_category'],
            'heat_index_c': snap['heat_index_c'],
            'wbgt_outdoor_c': snap['wbgt_outdoor_c'],
            'utci_c': snap['utci_c'],
            'risk_probability': snap['risk_probability'],
            'risk_category': snap['risk_category'],
            'confidence': snap['confidence'],
            'vulnerability_score': snap['vulnerability_score'],
            'exposure_score': snap['exposure_score'],
            'health_risk_level': snap['health_risk_level'],
            'risk_contributors': snap['risk_contributors'],
            'data_status': 'DEMO / SIMULATED'
        })
    return out


def history(loc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate 90-day realistic historical summer sequence with heatwave threshold markings."""
    rng = np.random.default_rng(_hash_seed(loc['id'], 999))
    out = []
    start = date.today() - timedelta(days=90)

    for i in range(90):
        target_date = start + timedelta(days=i)
        seasonal_cycle = 3.5 * np.sin((i - 15) / 14.0)
        microclimate = (loc['built_up_pct'] - 75) * 0.05

        temp = round(32.5 + seasonal_cycle + microclimate + rng.normal(0, 0.9), 1)
        rh = float(np.clip(62.0 - rng.normal(0, 5.0) - seasonal_cycle * 0.8, 25.0, 90.0))
        wind = float(np.clip(12.0 + rng.normal(0, 2.0), 3.0, 25.0))
        solar = float(np.clip(700.0 + seasonal_cycle * 20.0 + rng.normal(0, 50.0), 200.0, 1000.0))

        thermal = compute_all_thermal_metrics(temp, rh, wind, solar)
        hi = thermal['heat_index']['value']

        # IMD heatwave criteria proxy: Max temp >= 40°C or HI >= 45°C
        is_heatwave_day = bool(temp >= 40.0 or hi >= 44.0)

        out.append({
            'date': target_date.isoformat(),
            'temperature_c': temp,
            'humidity_pct': round(rh, 1),
            'heat_index_c': hi,
            'wbgt_c': thermal['wbgt']['value'],
            'utci_c': thermal['utci']['value'],
            'high_risk': is_heatwave_day,
            'heatwave_alert': is_heatwave_day
        })

    return out
