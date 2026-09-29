"""What-If Scenario Simulation Engine.

Enables disaster management authorities and hackathon judges to model the impact
of environmental shifts (e.g. +3°C heatwave escalation) and urban heat resilience
interventions (e.g. +25% green cover, cool roofs, emergency cooling shelters).
"""

from typing import Dict, Any
from ..thermal.engine import get_active_thermal_stress
from ..vulnerability.score import calculate_vulnerability_score, calculate_exposure_score
from ..risk.classifier import predict, risk_contributors


def run_what_if_simulation(
    base_snapshot: Dict[str, Any],
    delta_temperature_c: float = 0.0,
    delta_humidity_pct: float = 0.0,
    delta_green_cover_pct: float = 0.0,
    added_cooling_centers: int = 0,
    metric: str = 'heat_index'
) -> Dict[str, Any]:
    """Execute real-time counterfactual simulation comparing baseline vs simulated state."""
    # 1. Adjust environmental conditions (incorporating microclimate evaporative cooling from green canopy)
    canopy_cooling = delta_green_cover_pct * 0.05
    sim_temp = max(15.0, min(55.0, base_snapshot['temperature_c'] + delta_temperature_c - canopy_cooling))
    sim_rh = max(10.0, min(100.0, base_snapshot['humidity_pct'] + delta_humidity_pct))
    sim_wind = base_snapshot.get('wind_kmh', 10.0)
    sim_solar = base_snapshot.get('solar_w_m2', 650.0)

    # 2. Adjust urban resilience interventions
    sim_green = max(0.0, min(100.0, base_snapshot.get('green_cover_pct', 15.0) + delta_green_cover_pct))

    # Cooling centers reduce deficit: each cooling center reduces deficit by 3.5 points
    current_deficit = base_snapshot.get('cooling_access_deficit', 50.0)
    sim_deficit = max(5.0, current_deficit - (added_cooling_centers * 3.5))

    # Urban cooling microclimate effect: green cover reduces local LST anomaly
    current_lst = base_snapshot.get('lst_anomaly_c', 2.0)
    sim_lst = max(0.0, current_lst - (delta_green_cover_pct * 0.04))

    # 3. Recalculate Vulnerability and Exposure
    vuln_res = calculate_vulnerability_score(
        pop_density=base_snapshot['pop_density'],
        elderly_pct=base_snapshot['elderly_pct'],
        outdoor_worker_pct=base_snapshot['outdoor_worker_pct'],
        built_up_pct=base_snapshot['built_up_pct'],
        green_cover_pct=sim_green,
        lst_anomaly_c=sim_lst,
        cooling_access_deficit=sim_deficit
    )
    sim_vuln_score = vuln_res['score']
    sim_exposure_score = calculate_exposure_score(
        base_snapshot['pop_density'], base_snapshot['built_up_pct']
    )

    # 4. Recalculate Thermal Stress
    thermal_res = get_active_thermal_stress(
        temp_c=sim_temp,
        rh=sim_rh,
        wind_kmh=sim_wind,
        solar_w_m2=sim_solar,
        metric=metric
    )

    # 5. Recalculate AI Risk Model
    sim_features = {
        'temperature_c': sim_temp,
        'humidity_pct': sim_rh,
        'wind_kmh': sim_wind,
        'solar_w_m2': sim_solar,
        'heat_index_c': thermal_res['comparative']['heat_index_c'],
        'forecast_trend_c': base_snapshot.get('forecast_trend_c', 0.5),
        'vulnerability_score': sim_vuln_score,
        'exposure_score': sim_exposure_score,
        'heat_exposure_pct': sim_deficit
    }

    pred_res = predict(sim_features)
    sim_contributors = risk_contributors(sim_features)

    # Risk differential
    base_prob = base_snapshot.get('risk_probability', 0.5)
    prob_diff = round((pred_res['risk_probability'] - base_prob) * 100.0, 1)

    return {
        'baseline': {
            'temperature_c': base_snapshot['temperature_c'],
            'humidity_pct': base_snapshot['humidity_pct'],
            'green_cover_pct': base_snapshot.get('green_cover_pct', 15.0),
            'thermal_value_c': base_snapshot.get('heat_index_c', 35.0),
            'risk_probability': base_prob,
            'risk_category': base_snapshot.get('risk_category', 'MODERATE')
        },
        'simulated': {
            'temperature_c': round(sim_temp, 1),
            'humidity_pct': round(sim_rh, 1),
            'green_cover_pct': round(sim_green, 1),
            'thermal_value_c': thermal_res['value_c'],
            'thermal_category': thermal_res['category'],
            'vulnerability_score': sim_vuln_score,
            'exposure_score': sim_exposure_score,
            'risk_probability': pred_res['risk_probability'],
            'risk_category': pred_res['risk_category'],
            'confidence': pred_res['confidence'],
            'health_risk_level': pred_res['health_risk_level'],
            'risk_contributors': sim_contributors
        },
        'impact': {
            'risk_probability_delta_pct': prob_diff,
            'net_direction': 'increased' if prob_diff > 0 else 'reduced' if prob_diff < 0 else 'neutral',
            'summary': (
                f"Simulated interventions resulted in a {abs(prob_diff)}% "
                f"{'reduction' if prob_diff < 0 else 'increase'} in overall localized heat risk."
            )
        }
    }
