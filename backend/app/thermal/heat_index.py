"""NOAA/NWS Heat Index implementation.

The Rothfusz regression is an established Heat Index method for warm/humid
conditions. Values are returned in Celsius. Outside the normal regression
range, the simpler NWS adjustments are used. This is an apparent-temperature
indicator, not a medical diagnosis.
"""

import math
from typing import Dict, Any


def c_to_f(c: float) -> float:
    return c * 9 / 5 + 32


def f_to_c(f: float) -> float:
    return (f - 32) * 5 / 9


def heat_index_c(temp_c: float, rh: float) -> float:
    t = c_to_f(temp_c)
    r = max(0.0, min(100.0, rh))
    simple = 0.5 * (t + 61.0 + ((t - 68.0) * 1.2) + (r * 0.094))

    if t < 80.0 or r < 40.0:
        return round(f_to_c(simple), 1)

    hi = (
        -42.379 + 2.04901523 * t + 10.14333127 * r
        - 0.22475541 * t * r - 0.00683783 * t * t
        - 0.05481717 * r * r + 0.00122874 * t * t * r
        + 0.00085282 * t * r * r - 0.00000199 * t * t * r * r
    )

    if r < 13 and 80 <= t <= 112:
        adjustment = ((13 - r) / 4) * math.sqrt((17 - abs(t - 95)) / 17)
        hi -= adjustment
    elif r > 85 and 80 <= t <= 87:
        adjustment = ((r - 85) / 10) * ((87 - t) / 5)
        hi += adjustment
    return round(f_to_c(hi), 1)


def heat_index_category(hi_c: float) -> str:
    """NOAA National Weather Service (NWS) Heat Index risk categories."""
    if hi_c < 27.0:
        return 'LOW'          # Normal
    if hi_c < 32.0:
        return 'MODERATE'     # Caution (fatigue possible with prolonged exposure)
    if hi_c < 41.0:
        return 'HIGH'         # Extreme Caution (heat cramps and exhaustion likely)
    if hi_c < 54.0:
        return 'VERY HIGH'    # Danger (heat exhaustion likely, heat stroke possible)
    return 'EXTREME'          # Extreme Danger (heat stroke imminent)


def explain_heat_index(temp_c: float, rh: float) -> Dict[str, Any]:
    """Provide complete transparent breakdown of NOAA/NWS Heat Index."""
    t_f = c_to_f(temp_c)
    val = heat_index_c(temp_c, rh)
    val_f = c_to_f(val)
    cat = heat_index_category(val)

    impacts = {
        'LOW': 'Minimal risk of heat-related disorders during normal physical activities.',
        'MODERATE': 'Caution: Fatigue is possible with prolonged exposure and physical activity.',
        'HIGH': 'Extreme Caution: Heat cramps and heat exhaustion possible. Continued activity could lead to heat stroke.',
        'VERY HIGH': 'Danger: Heat cramps and heat exhaustion likely; heat stroke probable with continued exposure.',
        'EXTREME': 'Extreme Danger: Heat stroke or sunstroke highly likely with continued exposure.'
    }

    return {
        'metric_name': 'NOAA / NWS Heat Index',
        'standard': 'United States National Weather Service Apparent Temperature (Steadman / Rothfusz)',
        'value_c': val,
        'value_f': round(val_f, 1),
        'category': cat,
        'physiological_impact': impacts.get(cat, ''),
        'input_variables': {
            'dry_bulb_temperature': {'value': round(temp_c, 1), 'unit': '°C', 'fahrenheit': round(t_f, 1)},
            'relative_humidity': {'value': round(rh, 1), 'unit': '%'}
        },
        'formula': 'Rothfusz regression equation with Steadman linear fallback for mild conditions',
        'scientific_notes': 'Measures apparent temperature combining ambient heat and evaporative sweat impediment.'
    }
