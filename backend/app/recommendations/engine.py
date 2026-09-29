"""Action Recommendation Engine (Heat Action Plan - HAP).

Generates role-based, risk-calibrated operational guidance for 4 key stakeholder groups:
1. General Public & Vulnerable Citizens
2. Outdoor Workers, Delivery Riders & Informal Labor
3. Municipal Authorities & Urban Local Bodies (ULBs)
4. Hospitals, Clinics & Emergency Healthcare Facilities

All actions strictly follow established disaster management guidelines (NDMA / WHO / IMD HAP).
"""

from typing import Dict, Any, List


def recommendations(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Derive prioritized stakeholder action items based on localized thermal risk."""
    risk = snapshot.get('risk_category', 'LOW')
    outdoor_workers = snapshot.get('outdoor_worker_pct', 25.0)
    elderly = snapshot.get('elderly_pct', 10.0)
    vuln_score = snapshot.get('vulnerability_score', 50.0)
    humidity = snapshot.get('humidity_pct', 55.0)

    recs = []

    # 1. General Public
    public_actions = [
        'Maintain frequent oral hydration with water, lemon water, or ORS; avoid sugary and caffeinated drinks.',
        'Avoid direct sun exposure between 12:00 PM and 3:30 PM. Wear loose, light-colored cotton clothing.'
    ]
    if risk in {'VERY HIGH', 'EXTREME'}:
        public_actions.append('Check twice daily on elderly neighbors, infants, and individuals living alone without cooling.')
        public_actions.append('Use damp towels or cold foot baths if indoor air temperatures exceed 34°C without cross-ventilation.')
    elif risk == 'HIGH':
        public_actions.append('Plan all non-essential outdoor errands before 10:00 AM or after 5:00 PM.')

    recs.append({
        'audience': 'General Public & Citizens',
        'badge': 'Public Safety',
        'priority': 'Urgent' if risk in {'VERY HIGH', 'EXTREME'} else 'Recommended',
        'actions': public_actions
    })

    # 2. Outdoor Workers & Gig Economy
    worker_actions = []
    if risk in {'VERY HIGH', 'EXTREME'} or outdoor_workers >= 30:
        worker_actions.append(
            'Enforce mandatory 15-minute rest breaks every 45 minutes in designated shaded, ventilated rest hubs.'
        )
        worker_actions.append(
            'Reschedule heavy manual lifting and masonry work to cooler morning shifts (06:00-10:00).'
        )
        worker_actions.append(
            'Employers and platforms must supply chilled drinking water and electrolyte packets at worksites and delivery hubs.'
        )
    elif risk == 'HIGH':
        worker_actions.append('Provide continuous access to potable drinking water at outdoor job sites.')
        worker_actions.append('Mandate broad-brimmed hats or wet cloths covering the head and neck during direct sun exposure.')
    else:
        worker_actions.append('Standard hydration guidelines: consume at least 500ml water per hour of light physical exertion.')

    recs.append({
        'audience': 'Outdoor Workers & Labor',
        'badge': 'Occupational Health',
        'priority': 'Urgent' if risk in {'HIGH', 'VERY HIGH', 'EXTREME'} else 'Standard',
        'actions': worker_actions
    })

    # 3. Municipal Authorities & Urban Local Bodies (ULBs)
    ulb_actions = []
    if risk in {'VERY HIGH', 'EXTREME'} or vuln_score >= 65:
        ulb_actions.append(
            'Activate emergency public cooling centers in community halls, libraries, and temples with fans and drinking water.'
        )
        ulb_actions.append(
            'Deploy municipal mobile water tankers and misting stations across high-density informal settlement clusters.'
        )
        ulb_actions.append(
            'Coordinate with power distribution companies (DISCOMs) to guarantee zero unscheduled power cuts to domestic feeders.'
        )
    elif risk == 'HIGH':
        ulb_actions.append('Issue localized heat advisories via SMS, community loudspeakers, and ward control rooms.')
        ulb_actions.append('Inspect functioning of all public drinking water taps and fountains in transit hubs and markets.')
    else:
        ulb_actions.append('Maintain routine surveillance of ward water points and monitor 5-day heatwave forecast trends.')

    recs.append({
        'audience': 'Municipal Authorities & ULBs',
        'badge': 'Disaster Mitigation',
        'priority': 'High Priority' if risk in {'VERY HIGH', 'EXTREME'} else 'Preparedness',
        'actions': ulb_actions
    })

    # 4. Hospitals, PHCs & Emergency Medical Services
    health_actions = []
    if risk in {'VERY HIGH', 'EXTREME'} or elderly >= 12.0:
        health_actions.append(
            'Designate emergency rapid-cooling beds equipped with ice packs and cold water immersion equipment for exertional heat stroke.'
        )
        health_actions.append(
            'Stockpile emergency intravenous fluids (normal saline, Ringer lactate) and oral rehydration salts (ORS).'
        )
        health_actions.append(
            'Equip 108/emergency ambulances with cooling packs and train paramedical staff on early recognition of heat hyperpyrexia.'
        )
    else:
        health_actions.append('Review hospital heat-related illness registries and ensure adequate oral rehydration supplies.')

    recs.append({
        'audience': 'Hospitals & Health Facilities',
        'badge': 'Clinical Readiness',
        'priority': 'Urgent' if risk in {'VERY HIGH', 'EXTREME'} else 'Normal',
        'actions': health_actions
    })

    return recs
