"""Wet Bulb Globe Temperature (WBGT) estimation module.

Implements established meteorological and occupational approximations:
1. Natural Wet-Bulb Temperature (Tw) via Stull's psychrometric formulation (2011).
2. Globe Temperature (Tg) via Australian Bureau of Meteorology / Liljegren formulation
   incorporating solar irradiance (W/m^2) and wind speed (m/s).
3. Outdoor WBGT: 0.7 * Tw + 0.2 * Tg + 0.1 * T_air (ISO 7243 standard).
4. Indoor/Shaded WBGT: 0.7 * Tw + 0.3 * T_air.

Thresholds correspond to ISO 7243 and ACGIH occupational work-rest guidelines.
"""

import math
from typing import Dict, Any


def stull_wet_bulb_c(temp_c: float, rh: float) -> float:
    """Stull (2011) formula for wet-bulb temperature in Celsius.
    Valid for RH between 5% and 99% and temperatures between -20C and 50C.
    """
    t = float(temp_c)
    r = float(max(5.0, min(99.0, rh)))
    
    tw = (
        t * math.atan(0.151977 * math.sqrt(r + 8.313659))
        + math.atan(t + r)
        - math.atan(r - 1.676331)
        + 0.00391838 * (r ** 1.5) * math.atan(0.023101 * r)
        - 4.686035
    )
    return float(tw)


def estimate_globe_temp_c(temp_c: float, wind_ms: float, solar_w_m2: float) -> float:
    """Estimate black globe temperature Tg from dry-bulb temp, wind, and solar irradiance.
    Australian Bureau of Meteorology / Liljegren empirical relation.
    """
    v = max(0.2, float(wind_ms))
    s = max(0.0, float(solar_w_m2))
    
    # Solar heating offset with wind cooling convective damping
    # In full sun (800 W/m2) and low wind (1 m/s), Tg can be 10-15°C above T_air.
    solar_offset = (s * 0.0135) / (1.0 + 0.38 * (v ** 0.58))
    return float(temp_c + solar_offset)


def wbgt_c(
    temp_c: float,
    rh: float,
    wind_kmh: float = 10.0,
    solar_w_m2: float = 600.0,
    outdoor: bool = True
) -> float:
    """Calculate Wet Bulb Globe Temperature (WBGT) in Celsius."""
    tw = stull_wet_bulb_c(temp_c, rh)
    wind_ms = max(0.1, wind_kmh / 3.6)
    
    if outdoor and solar_w_m2 > 0:
        tg = estimate_globe_temp_c(temp_c, wind_ms, solar_w_m2)
        wbgt = 0.7 * tw + 0.2 * tg + 0.1 * temp_c
    else:
        # Indoor or shaded conditions (no solar radiation)
        wbgt = 0.7 * tw + 0.3 * temp_c
        
    return float(round(wbgt, 1))


def wbgt_category(wbgt_val: float) -> str:
    """ISO 7243 / ACGIH occupational thermal stress classification."""
    if wbgt_val < 26.0:
        return 'LOW'
    if wbgt_val < 29.0:
        return 'MODERATE'
    if wbgt_val < 31.0:
        return 'HIGH'
    if wbgt_val < 33.0:
        return 'VERY HIGH'
    return 'EXTREME'


def wbgt_work_rest_cycle(category: str) -> str:
    """ACGIH recommended work-rest guidelines for heavy/moderate manual labor."""
    cycles = {
        'LOW': 'Continuous work permitted (100% work / normal breaks). Hydration at regular intervals.',
        'MODERATE': '75% work / 25% rest each hour in shade. Provide 500ml water per hour.',
        'HIGH': '50% work / 50% rest each hour in shaded, ventilated area. Active monitoring required.',
        'VERY HIGH': '25% work / 75% rest each hour. Postpone strenuous labor to cooler hours.',
        'EXTREME': 'Cease non-emergency outdoor manual physical labor. High risk of exertional heat stroke.'
    }
    return cycles.get(category, cycles['LOW'])


def explain_wbgt(
    temp_c: float,
    rh: float,
    wind_kmh: float = 10.0,
    solar_w_m2: float = 600.0,
    outdoor: bool = True
) -> Dict[str, Any]:
    """Provide complete transparent breakdown of the WBGT calculation."""
    tw = stull_wet_bulb_c(temp_c, rh)
    wind_ms = wind_kmh / 3.6
    tg = estimate_globe_temp_c(temp_c, wind_ms, solar_w_m2) if outdoor else temp_c
    val = wbgt_c(temp_c, rh, wind_kmh, solar_w_m2, outdoor)
    cat = wbgt_category(val)
    
    return {
        'metric_name': 'Wet Bulb Globe Temperature (WBGT)',
        'standard': 'ISO 7243 / ACGIH Occupational Heat Stress Standard',
        'value_c': val,
        'category': cat,
        'regime': 'Outdoor with direct solar radiation' if outdoor else 'Indoor / Shaded environment',
        'input_variables': {
            'dry_bulb_temperature': {'value': round(temp_c, 1), 'unit': '°C'},
            'relative_humidity': {'value': round(rh, 1), 'unit': '%'},
            'wind_speed': {'value': round(wind_kmh, 1), 'unit': 'km/h', 'wind_ms': round(wind_ms, 2)},
            'solar_irradiance': {'value': round(solar_w_m2, 1), 'unit': 'W/m²'}
        },
        'intermediate_values': {
            'natural_wet_bulb_c': round(tw, 2),
            'black_globe_temp_c': round(tg, 2)
        },
        'formula': '0.7 * Tw + 0.2 * Tg + 0.1 * T_air' if outdoor else '0.7 * Tw + 0.3 * T_air',
        'work_rest_recommendation': wbgt_work_rest_cycle(cat)
    }
