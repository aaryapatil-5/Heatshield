"""Unified Thermal Stress Engine.

Provides multi-metric human thermal stress intelligence supporting:
1. NOAA/NWS Heat Index (temperature + humidity)
2. Wet Bulb Globe Temperature - WBGT (temperature + humidity + wind + solar radiation)
3. Universal Thermal Climate Index - UTCI (biometeorological human heat balance)

Allows seamless switching between metrics while ensuring absolute transparency on formulas,
data requirements, and operational safety thresholds.
"""

from typing import Dict, Any, Optional
from .heat_index import heat_index_c, heat_index_category, explain_heat_index
from .wbgt import wbgt_c, wbgt_category, explain_wbgt
from .utci import utci_approx_c, utci_category, explain_utci


AVAILABLE_METRICS = {
    'heat_index': {
        'id': 'heat_index',
        'name': 'NOAA Heat Index',
        'short_name': 'Heat Index',
        'unit': '°C',
        'description': 'Measures apparent temperature from ambient temperature and relative humidity.',
        'required_variables': ['temperature_c', 'humidity_pct']
    },
    'wbgt': {
        'id': 'wbgt',
        'name': 'Wet Bulb Globe Temperature',
        'short_name': 'WBGT',
        'unit': '°C',
        'description': 'Gold-standard occupational heat stress index accounting for sun radiation and wind.',
        'required_variables': ['temperature_c', 'humidity_pct', 'wind_kmh', 'solar_w_m2']
    },
    'utci': {
        'id': 'utci',
        'name': 'Universal Thermal Climate Index',
        'short_name': 'UTCI',
        'unit': '°C',
        'description': 'Physiological equivalent temperature based on multi-node human thermoregulation model.',
        'required_variables': ['temperature_c', 'humidity_pct', 'wind_kmh', 'solar_w_m2']
    }
}


def compute_all_thermal_metrics(
    temp_c: float,
    rh: float,
    wind_kmh: float = 10.0,
    solar_w_m2: float = 650.0
) -> Dict[str, Any]:
    """Calculate all thermal indices simultaneously for comparative assessment."""
    hi_val = heat_index_c(temp_c, rh)
    hi_cat = heat_index_category(hi_val)

    wbgt_val = wbgt_c(temp_c, rh, wind_kmh, solar_w_m2, outdoor=True)
    wbgt_cat = wbgt_category(wbgt_val)

    wbgt_indoor_val = wbgt_c(temp_c, rh, wind_kmh, solar_w_m2=0.0, outdoor=False)
    wbgt_indoor_cat = wbgt_category(wbgt_indoor_val)

    utci_val = utci_approx_c(temp_c, rh, wind_kmh, solar_w_m2)
    utci_cat = utci_category(utci_val)

    return {
        'heat_index': {
            'value': hi_val,
            'category': hi_cat,
            'unit': '°C',
            'explanation': explain_heat_index(temp_c, rh)
        },
        'wbgt': {
            'value': wbgt_val,
            'category': wbgt_cat,
            'unit': '°C',
            'indoor_value': wbgt_indoor_val,
            'indoor_category': wbgt_indoor_cat,
            'explanation': explain_wbgt(temp_c, rh, wind_kmh, solar_w_m2, outdoor=True)
        },
        'utci': {
            'value': utci_val,
            'category': utci_cat,
            'unit': '°C',
            'explanation': explain_utci(temp_c, rh, wind_kmh, solar_w_m2)
        }
    }


def get_active_thermal_stress(
    temp_c: float,
    rh: float,
    wind_kmh: float = 10.0,
    solar_w_m2: float = 650.0,
    metric: str = 'heat_index'
) -> Dict[str, Any]:
    """Retrieve thermal stress assessment using the designated active metric."""
    all_metrics = compute_all_thermal_metrics(temp_c, rh, wind_kmh, solar_w_m2)
    chosen_key = metric if metric in AVAILABLE_METRICS else 'heat_index'
    active_data = all_metrics[chosen_key]

    return {
        'active_metric': chosen_key,
        'metric_meta': AVAILABLE_METRICS[chosen_key],
        'value_c': active_data['value'],
        'category': active_data['category'],
        'explanation': active_data['explanation'],
        'comparative': {
            'heat_index_c': all_metrics['heat_index']['value'],
            'heat_index_category': all_metrics['heat_index']['category'],
            'wbgt_outdoor_c': all_metrics['wbgt']['value'],
            'wbgt_outdoor_category': all_metrics['wbgt']['category'],
            'utci_c': all_metrics['utci']['value'],
            'utci_category': all_metrics['utci']['category']
        }
    }
