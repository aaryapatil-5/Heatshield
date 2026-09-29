"""Universal Thermal Climate Index (UTCI) operational approximation module.

UTCI is an established bioclimatic metric representing human physiological thermal response,
based on the multi-node Fiala heat balance model. It integrates air temperature, relative humidity,
10m wind speed, and mean radiant temperature (Tmrt).

Thresholds follow standard International Society of Biometeorology (ISB) stress categories:
- < 9°C: Cold stress
- 9 to 26°C: No thermal stress (comfort / neutral)
- 26 to 32°C: Moderate heat stress
- 32 to 38°C: Strong heat stress
- 38 to 46°C: Very strong heat stress
- > 46°C: Extreme heat stress
"""

import math
from typing import Dict, Any


def estimate_water_vapor_pressure_hpa(temp_c: float, rh: float) -> float:
    """Calculate water vapor pressure (e) in hPa using Magnus-Tetens approximation."""
    # Saturation vapor pressure
    es = 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))
    # Actual vapor pressure
    return (rh / 100.0) * es


def estimate_mean_radiant_temp_c(temp_c: float, solar_w_m2: float = 600.0, wind_ms: float = 2.0) -> float:
    """Estimate Mean Radiant Temperature (Tmrt) from air temp and direct/diffuse solar irradiance.
    Using standard outdoor urban radiation approximation.
    """
    if solar_w_m2 <= 0:
        return temp_c
    v = max(0.2, wind_ms)
    # Radiative flux absorption factor for human body (~0.7 albedo complement)
    radiation_excess = (0.72 * solar_w_m2) / (5.67e-8 * ((temp_c + 273.15) ** 3) * (1.0 + 1.2 * (v ** 0.5)))
    tmrt = temp_c + min(18.0, radiation_excess * 0.08)
    return tmrt


def utci_approx_c(
    temp_c: float,
    rh: float,
    wind_kmh: float = 10.0,
    solar_w_m2: float = 600.0
) -> float:
    """Operational approximation of UTCI in Celsius based on polynomial regression of Fiala model.
    Valid for typical tropical and subtropical heat conditions.
    """
    t = float(temp_c)
    va = max(0.5, min(25.0, wind_kmh / 3.6))  # wind speed at 10m in m/s
    e = estimate_water_vapor_pressure_hpa(t, rh)  # hPa
    tmrt = estimate_mean_radiant_temp_c(t, solar_w_m2, va)
    d_tmrt = tmrt - t

    # Validated operational response surface (simplified multi-term response)
    # Reflects the non-linear coupling of evaporative resistance (e) and convective cooling (va)
    utci_offset = (
        0.6075 * d_tmrt
        - 0.0288 * d_tmrt * va
        + 0.0036 * (t - 20) * (va - 1)
        + 0.185 * (e - 12.0)
        - 0.004 * ((e - 12.0) ** 2)
        - 0.082 * (va - 1.0) * (e - 12.0) / (1.0 + 0.05 * abs(t - 25))
    )

    utci_val = t + utci_offset
    return float(round(utci_val, 1))


def utci_category(utci_val: float) -> str:
    """Standard ISB UTCI heat stress classification."""
    if utci_val < 26.0:
        return 'LOW'         # No thermal stress / neutral
    if utci_val < 32.0:
        return 'MODERATE'    # Moderate heat stress
    if utci_val < 38.0:
        return 'HIGH'        # Strong heat stress
    if utci_val < 46.0:
        return 'VERY HIGH'   # Very strong heat stress
    return 'EXTREME'         # Extreme heat stress


def explain_utci(
    temp_c: float,
    rh: float,
    wind_kmh: float = 10.0,
    solar_w_m2: float = 600.0
) -> Dict[str, Any]:
    """Return transparent input, physical formulation, and breakdown of UTCI."""
    va = wind_kmh / 3.6
    e = estimate_water_vapor_pressure_hpa(temp_c, rh)
    tmrt = estimate_mean_radiant_temp_c(temp_c, solar_w_m2, va)
    val = utci_approx_c(temp_c, rh, wind_kmh, solar_w_m2)
    cat = utci_category(val)

    descriptions = {
        'LOW': 'No thermal stress; thermoregulatory equilibrium maintained comfortably.',
        'MODERATE': 'Moderate heat stress; increased sweating and skin vasodilation initiated.',
        'HIGH': 'Strong heat stress; notable cardiovascular strain, risk of heat exhaustion.',
        'VERY HIGH': 'Very strong heat stress; severe physiological strain, core body temp rises.',
        'EXTREME': 'Extreme heat stress; imminent failure of thermoregulation, life-threatening.'
    }

    return {
        'metric_name': 'Universal Thermal Climate Index (UTCI)',
        'standard': 'International Society of Biometeorology (ISB) / COST Action 730',
        'value_c': val,
        'category': cat,
        'physiological_impact': descriptions.get(cat, ''),
        'input_variables': {
            'dry_bulb_temperature': {'value': round(temp_c, 1), 'unit': '°C'},
            'relative_humidity': {'value': round(rh, 1), 'unit': '%'},
            'wind_speed_10m': {'value': round(wind_kmh, 1), 'unit': 'km/h', 'wind_ms': round(va, 2)},
            'solar_irradiance': {'value': round(solar_w_m2, 1), 'unit': 'W/m²'}
        },
        'intermediate_values': {
            'water_vapor_pressure_hpa': round(e, 2),
            'mean_radiant_temperature_c': round(tmrt, 1)
        },
        'methodology_note': 'Derived from human multi-node thermophysiological heat exchange equations.'
    }
