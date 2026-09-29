"""GIS Spatial Grid & GeoJSON Feature Collection Service.

Generates standard RFC 7946 compliant GeoJSON Polygons for localized urban wards
and grid cells across Mumbai, Delhi, and Ahmedabad.
Structured for direct replacement with official Municipal Corporation administrative shapefiles.
"""

from typing import List, Dict, Any
import numpy as np


def generate_ward_polygon(lat: float, lon: float, ward_id: str, radius_km: float = 1.6) -> List[List[float]]:
    """Generate realistic closed polygon boundary around ward centroid."""
    # Convert km radius to approximate degrees (1 deg lat ~ 111 km, 1 deg lon ~ 104 km in central India)
    d_lat = radius_km / 111.0
    d_lon = radius_km / (111.0 * np.cos(np.radians(lat)))

    # Use deterministic pseudo-random offsets for organic administrative boundary shapes
    h = sum(ord(c) for c in ward_id)
    rng = np.random.default_rng(h)

    num_vertices = 8
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    coords = []

    for angle in angles:
        # Radial jitter to emulate natural municipal ward perimeter
        jitter = 0.85 + 0.30 * rng.random()
        p_lat = lat + d_lat * np.sin(angle) * jitter
        p_lon = lon + d_lon * np.cos(angle) * jitter
        coords.append([round(float(p_lon), 6), round(float(p_lat), 6)])

    # Close the ring
    coords.append(coords[0])
    return coords


def feature_collection(location_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert location snapshots into GeoJSON FeatureCollection with comprehensive properties."""
    features = []

    for snap in location_snapshots:
        coords = generate_ward_polygon(
            lat=snap['lat'],
            lon=snap['lon'],
            ward_id=snap['id'],
            radius_km=1.5
        )

        props = {
            'id': snap['id'],
            'name': snap['name'],
            'city': snap.get('city', 'Mumbai'),
            'district': snap['district'],
            'lat': snap['lat'],
            'lon': snap['lon'],
            'temperature_c': snap['temperature_c'],
            'humidity_pct': snap['humidity_pct'],
            'heat_index_c': snap.get('heat_index_c', snap['temperature_c']),
            'wbgt_outdoor_c': snap.get('wbgt_outdoor_c', 0.0),
            'utci_c': snap.get('utci_c', 0.0),
            'thermal_category': snap.get('thermal_category', 'MODERATE'),
            'vulnerability_score': snap['vulnerability_score'],
            'exposure_score': snap['exposure_score'],
            'built_up_pct': snap.get('built_up_pct', 80),
            'green_cover_pct': snap.get('green_cover_pct', 15),
            'pop_density': snap['pop_density'],
            'risk_category': snap['risk_category'],
            'risk_probability': snap['risk_probability'],
            'confidence': snap['confidence'],
            'health_risk_level': snap.get('health_risk_level', 'Moderate'),
            'data_status': snap.get('data_status', 'DEMO / SIMULATED'),
            'is_escalating': snap.get('is_escalating', False)
        }

        features.append({
            'type': 'Feature',
            'id': snap['id'],
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            },
            'properties': props
        })

    return {
        'type': 'FeatureCollection',
        'features': features
    }
