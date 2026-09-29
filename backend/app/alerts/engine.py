"""Early Warning & Alert Generation Engine.

Synthesizes physical thermal stress thresholds, AI risk probabilities,
and multi-day forecast trajectories to trigger prioritized decision-support alerts.
Every alert is explicitly tagged as a prototype decision-support notification.
"""

from typing import Dict, Any, List


def build_alerts(snapshot: Dict[str, Any], forecast_days: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate structured multi-tiered early warning alerts."""
    alerts = []
    current_risk = snapshot.get('risk_category', 'LOW')
    current_prob = snapshot.get('risk_probability', 0.0)
    ward_name = snapshot.get('name', 'Selected Area')
    city = snapshot.get('city', 'Urban Region')
    hi = snapshot.get('heat_index_c', snapshot.get('temperature_c', 35.0))
    wbgt = snapshot.get('wbgt_outdoor_c', 30.0)

    # 1. Current Condition Alert
    if current_risk in {'HIGH', 'VERY HIGH', 'EXTREME'}:
        severity_map = {
            'HIGH': 'ADVISORY',
            'VERY HIGH': 'WARNING',
            'EXTREME': 'EMERGENCY'
        }
        severity_code = severity_map.get(current_risk, 'ADVISORY')

        drivers = snapshot.get('risk_contributors', [])
        driver_str = ', '.join(f"{d['factor']} ({d['contribution_pct']}%)" for d in drivers[:3]) if drivers else 'High thermal load and dense built-up environment'

        action_map = {
            'HIGH': 'Encourage frequent hydration, minimize unshaded outdoor physical exertion between 12:00-15:00.',
            'VERY HIGH': 'Enforce mandatory shaded rest intervals for outdoor workers; activate municipal cooling points.',
            'EXTREME': 'EMERGENCY PROTOCOL: Suspend non-critical manual outdoor labor; open emergency cooling shelters and deploy water tankers.'
        }

        alerts.append({
            'id': f"alert-curr-{snapshot['id']}",
            'severity': severity_code,
            'risk_category': current_risk,
            'title': f"Prototype AI Alert: {severity_code.title()} Level ({current_risk})",
            'affected_area': f"{ward_name}, {city}",
            'valid_time': 'Immediate / Current Observation Window',
            'thermal_summary': f"Apparent Heat Index: {hi:.1f}°C | WBGT Outdoor: {wbgt:.1f}°C",
            'risk_probability_pct': round(current_prob * 100),
            'scientific_reason': f"Compounding drivers: {driver_str}.",
            'recommended_action': action_map.get(current_risk, 'Maintain hydration and seek shaded areas.'),
            'is_official': False,
            'disclaimer': 'Prototype AI Alert — Decision Support Only — Not an Official IMD Bulletin'
        })

    # 2. Multi-Day Forecast Trajectory Alerts (Early Warning)
    # Detect escalating heatwave sequence
    high_future_days = [d for d in forecast_days if d.get('risk_category') in {'VERY HIGH', 'EXTREME'}]

    if len(high_future_days) >= 2:
        lead_day = high_future_days[0]
        peak_day = max(high_future_days, key=lambda d: d.get('temperature_c', 0.0))
        alerts.append({
            'id': f"alert-multi-{snapshot['id']}",
            'severity': 'EMERGENCY' if any(d.get('risk_category') == 'EXTREME' for d in high_future_days) else 'WARNING',
            'risk_category': peak_day['risk_category'],
            'title': '3–5 Day Extreme Heatwave Wave Early Warning',
            'affected_area': f"{ward_name}, {city}",
            'valid_time': f"Projected from {lead_day['day_label']} through {high_future_days[-1]['day_label']}",
            'thermal_summary': f"Peak Forecast Temp: {peak_day['temperature_c']:.1f}°C | Peak Heat Index: {peak_day['heat_index_c']:.1f}°C",
            'risk_probability_pct': round(peak_day['risk_probability'] * 100),
            'scientific_reason': (
                f"Multi-day thermal accumulation detected across {len(high_future_days)} consecutive days. "
                f"Night-time radiative cooling is impeded by {snapshot.get('built_up_pct', 85)}% built-up density."
            ),
            'recommended_action': (
                'Municipal Local Bodies (ULBs) should pre-activate Heat Action Plan (HAP) Tier 2/3 protocols. '
                'Notify hospitals to ready cold-immersion units and stock oral rehydration solutions.'
            ),
            'is_official': False,
            'disclaimer': 'Prototype AI Alert — Decision Support Only — Not an Official IMD Bulletin'
        })
    elif len(high_future_days) == 1:
        day = high_future_days[0]
        alerts.append({
            'id': f"alert-single-{snapshot['id']}",
            'severity': 'WARNING',
            'risk_category': day['risk_category'],
            'title': f"Early Warning: Severe Heat Spike Projected for {day['day_label']}",
            'affected_area': f"{ward_name}, {city}",
            'valid_time': day['day_label'],
            'thermal_summary': f"Forecast Temp: {day['temperature_c']:.1f}°C | Heat Index: {day['heat_index_c']:.1f}°C",
            'risk_probability_pct': round(day['risk_probability'] * 100),
            'scientific_reason': 'Anticipated sharp spike in ambient temperature coupled with elevated relative humidity.',
            'recommended_action': 'Schedule outdoor municipal and construction work in early morning shifts (06:00-10:00).',
            'is_official': False,
            'disclaimer': 'Prototype AI Alert — Decision Support Only — Not an Official IMD Bulletin'
        })

    return alerts
