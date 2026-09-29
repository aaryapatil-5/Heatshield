"""FastAPI Routes for HeatShield AI.

Provides RESTful endpoints for:
- Mode toggling (Demo / Live)
- Multi-city and ward location queries
- Physical thermal stress (Heat Index, WBGT, UTCI)
- 5-Day early warning forecasting
- GIS GeoJSON polygon risk map
- Tiered AI alerts and Heat Action Plan recommendations
- Historical 90-day time-series
- Model performance and temporal validation metrics
- 'What-If' scenario simulation engine
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..services.demo_data import LOCATIONS, location_snapshot, forecast, history
from ..services.weather import WEATHER
from ..services.simulation import run_what_if_simulation
from ..thermal.engine import AVAILABLE_METRICS, compute_all_thermal_metrics, get_active_thermal_stress
from ..alerts.engine import build_alerts
from ..recommendations.engine import recommendations
from ..risk.classifier import predict as ml_predict, risk_contributors, BUNDLE
from ..gis.grid import feature_collection

router = APIRouter(prefix='/api')
CURRENT_MODE = 'demo'  # 'demo' or 'live'
DEFAULT_METRIC = 'heat_index'  # 'heat_index', 'wbgt', or 'utci'


class ModeRequest(BaseModel):
    mode: str = Field(..., pattern='^(demo|live)$')


class SimulationRequest(BaseModel):
    location_id: str = 'ward-dharavi'
    delta_temperature_c: float = 0.0
    delta_humidity_pct: float = 0.0
    delta_green_cover_pct: float = 0.0
    added_cooling_centers: int = 0
    metric: str = 'heat_index'


class PredictRequest(BaseModel):
    temperature_c: float
    humidity_pct: float
    wind_kmh: float = 10.0
    solar_w_m2: float = 650.0
    heat_index_c: Optional[float] = None
    forecast_trend_c: float = 0.5
    vulnerability_score: float = 50.0
    exposure_score: float = 50.0
    heat_exposure_pct: float = 50.0


def resolve_location(location_query: str) -> Dict[str, Any]:
    """Find location by ID, slug, or case-insensitive name."""
    norm = location_query.strip().lower()
    for loc in LOCATIONS:
        if loc['id'].lower() == norm or loc['name'].lower() == norm or loc['name'].lower().startswith(norm):
            return loc
    raise HTTPException(status_code=404, detail=f"Location '{location_query}' not found in registry.")


@router.get('/health')
def health():
    return {
        'status': 'ok',
        'service': 'HeatShield AI Core Intelligence API',
        'version': '1.0.0',
        'system': 'operational'
    }


@router.get('/mode')
def get_mode():
    return {
        'mode': CURRENT_MODE,
        'live_available': True,
        'default_thermal_metric': DEFAULT_METRIC,
        'description': (
            'Demo mode utilizes deterministic, scientifically grounded simulations (seed 26083) '
            'with zero external API key requirements.'
            if CURRENT_MODE == 'demo' else
            'Live weather is actively queried from Open-Meteo API. Automatic fallback to Demo mode if network fails.'
        )
    }


@router.post('/mode')
def set_mode(payload: ModeRequest):
    global CURRENT_MODE
    CURRENT_MODE = payload.mode
    return {
        'mode': CURRENT_MODE,
        'status': f"Switched to {CURRENT_MODE.upper()} mode successfully."
    }


@router.get('/thermal-metrics')
def list_thermal_metrics():
    """List supported human thermal stress indices with metadata and required variables."""
    return {
        'active_default': DEFAULT_METRIC,
        'metrics': AVAILABLE_METRICS
    }


@router.get('/locations')
def list_locations(city: Optional[str] = Query(None, description='Filter locations by city/region')):
    """Retrieve available wards/monitoring zones, optionally filtered by city."""
    filtered = LOCATIONS
    if city:
        filtered = [l for l in LOCATIONS if l.get('city', '').lower() == city.lower()]
    return [
        {
            'id': l['id'],
            'city': l.get('city', 'Mumbai'),
            'name': l['name'],
            'district': l['district'],
            'lat': l['lat'],
            'lon': l['lon'],
            'pop_density': l['pop_density'],
            'built_up_pct': l['built_up_pct'],
            'green_cover_pct': l['green_cover_pct'],
            'is_escalating': l.get('is_escalating_heatwave', False),
            'description': l.get('description', '')
        }
        for l in filtered
    ]


@router.get('/current-risk')
def get_current_risk(
    location: str = Query('ward-dharavi'),
    metric: str = Query('heat_index', description='heat_index, wbgt, or utci')
):
    """Retrieve full current conditions, thermal stress, vulnerability, and AI risk prediction."""
    loc = resolve_location(location)
    snap = location_snapshot(loc, day_offset=0, metric=metric)

    if CURRENT_MODE == 'live':
        try:
            live = WEATHER.live_current(loc['lat'], loc['lon'], metric=metric)
            snap.update(live)
            # Recompute ML prediction with live inputs
            features = {
                'temperature_c': snap['temperature_c'],
                'humidity_pct': snap['humidity_pct'],
                'wind_kmh': snap['wind_kmh'],
                'solar_w_m2': snap.get('solar_w_m2', 650.0),
                'heat_index_c': snap.get('heat_index_c', snap['temperature_c']),
                'forecast_trend_c': 0.4,
                'vulnerability_score': snap['vulnerability_score'],
                'exposure_score': snap['exposure_score'],
                'heat_exposure_pct': loc.get('cooling_access_deficit', 50.0)
            }
            ml_res = ml_predict(features)
            snap.update(ml_res)
            snap['risk_contributors'] = risk_contributors(features)
            snap['data_status'] = 'LIVE / OPEN-METEO'
        except Exception as e:
            snap['data_status'] = 'DEMO FALLBACK'
            snap['live_error'] = f"Live weather query failed ({str(e)}). Displaying deterministic fallback."

    return snap


@router.get('/forecast')
def get_forecast(
    location: str = Query('ward-dharavi'),
    metric: str = Query('heat_index')
):
    """Retrieve 5-day risk and thermal forecast."""
    loc = resolve_location(location)

    if CURRENT_MODE == 'live':
        try:
            live_days = WEATHER.live_forecast(loc['lat'], loc['lon'], metric=metric)
            # Enrich live forecast with ML risk prediction
            enriched = []
            for d in live_days:
                features = {
                    'temperature_c': d['temperature_c'],
                    'humidity_pct': d['humidity_pct'],
                    'wind_kmh': d['wind_kmh'],
                    'solar_w_m2': d.get('solar_w_m2', 650.0),
                    'heat_index_c': d['heat_index_c'],
                    'forecast_trend_c': 0.5,
                    'vulnerability_score': loc.get('built_up_pct', 80) * 0.7,
                    'exposure_score': loc.get('pop_density', 30000) / 600,
                    'heat_exposure_pct': 50.0
                }
                pred = ml_predict(features)
                enriched.append({
                    **d,
                    'risk_probability': pred['risk_probability'],
                    'risk_category': pred['risk_category'],
                    'confidence': pred['confidence'],
                    'vulnerability_score': round(features['vulnerability_score'], 1),
                    'exposure_score': round(features['exposure_score'], 1),
                    'risk_contributors': risk_contributors(features)
                })
            return {
                'location': loc['name'],
                'city': loc.get('city', 'Mumbai'),
                'data_status': 'LIVE / OPEN-METEO',
                'active_metric': metric,
                'forecast': enriched
            }
        except Exception:
            pass

    return {
        'location': loc['name'],
        'city': loc.get('city', 'Mumbai'),
        'data_status': 'DEMO / SIMULATED',
        'active_metric': metric,
        'forecast': forecast(loc, metric=metric)
    }


@router.get('/risk-map')
def get_risk_map(
    city: Optional[str] = Query(None),
    metric: str = Query('heat_index')
):
    """Return standard GeoJSON FeatureCollection of ward boundaries and current risk properties."""
    target_locations = LOCATIONS
    if city:
        target_locations = [l for l in LOCATIONS if l.get('city', '').lower() == city.lower()]
    snaps = [location_snapshot(l, day_offset=0, metric=metric) for l in target_locations]
    geo = feature_collection(snaps)
    return {
        'type': 'FeatureCollection',
        'features': geo['features'],
        'data_status': 'DEMO / SIMULATED' if CURRENT_MODE == 'demo' else 'LIVE / MIXED'
    }


@router.get('/location/{id}')
def get_location_by_id(id: str, metric: str = Query('heat_index')):
    loc = resolve_location(id)
    return location_snapshot(loc, day_offset=0, metric=metric)


@router.get('/history')
def get_historical_trends(location: str = Query('ward-dharavi')):
    """Retrieve 90-day historical time-series for seasonal heatwave analysis."""
    loc = resolve_location(location)
    return {
        'location': loc['name'],
        'city': loc.get('city', 'Mumbai'),
        'data_status': 'DEMO / SIMULATED',
        'history': history(loc)
    }


@router.get('/alerts')
def get_alerts(location: str = Query('ward-dharavi'), metric: str = Query('heat_index')):
    """Retrieve active early warning alerts and emergency advisories."""
    loc = resolve_location(location)
    snap = location_snapshot(loc, day_offset=0, metric=metric)
    fc = forecast(loc, metric=metric)
    return {
        'location': loc['name'],
        'alerts': build_alerts(snap, fc),
        'data_status': snap['data_status']
    }


@router.get('/recommendations')
def get_recommendations(location: str = Query('ward-dharavi'), metric: str = Query('heat_index')):
    """Retrieve role-based Heat Action Plan guidance."""
    loc = resolve_location(location)
    snap = location_snapshot(loc, day_offset=0, metric=metric)
    return {
        'location': loc['name'],
        'recommendations': recommendations(snap),
        'data_status': snap['data_status']
    }


@router.get('/model-performance')
def get_model_performance():
    """Retrieve scientific validation metrics, feature importances, and calibration curve."""
    return {
        'model_name': 'Random Forest Heat-Risk Ensemble Classifier',
        'n_estimators': 180,
        'features': [
            'temperature_c', 'humidity_pct', 'wind_kmh', 'solar_w_m2',
            'heat_index_c', 'forecast_trend_c', 'vulnerability_score',
            'exposure_score', 'heat_exposure_pct'
        ],
        'metrics': BUNDLE.metrics,
        'feature_importances': BUNDLE.importances,
        'calibration': BUNDLE.calibration_data,
        'validation_methodology': 'Temporal backtesting split on deterministic simulated prototype cohort (seed 26083)',
        'official_disclaimer': (
            'Prototype validation metrics evaluate model calibration on simulated data. '
            'Real-world operational accreditation requires longitudinal IMD/MoES weather station archives.'
        )
    }


@router.post('/predict')
def run_custom_prediction(payload: PredictRequest):
    """Execute AI risk prediction for a custom feature vector."""
    hi = payload.heat_index_c
    if hi is None:
        from ..thermal.heat_index import heat_index_c
        hi = heat_index_c(payload.temperature_c, payload.humidity_pct)

    features = {
        'temperature_c': payload.temperature_c,
        'humidity_pct': payload.humidity_pct,
        'wind_kmh': payload.wind_kmh,
        'solar_w_m2': payload.solar_w_m2,
        'heat_index_c': hi,
        'forecast_trend_c': payload.forecast_trend_c,
        'vulnerability_score': payload.vulnerability_score,
        'exposure_score': payload.exposure_score,
        'heat_exposure_pct': payload.heat_exposure_pct
    }
    pred = ml_predict(features)
    pred['risk_contributors'] = risk_contributors(features)
    return pred


@router.post('/simulate')
def simulate_scenario(payload: SimulationRequest):
    """Execute What-If counterfactual scenario testing climate shifts and urban resilience interventions."""
    loc = resolve_location(payload.location_id)
    base_snap = location_snapshot(loc, day_offset=0, metric=payload.metric)
    result = run_what_if_simulation(
        base_snapshot=base_snap,
        delta_temperature_c=payload.delta_temperature_c,
        delta_humidity_pct=payload.delta_humidity_pct,
        delta_green_cover_pct=payload.delta_green_cover_pct,
        added_cooling_centers=payload.added_cooling_centers,
        metric=payload.metric
    )
    return {
        'location': loc['name'],
        'city': loc.get('city', 'Mumbai'),
        'simulation': result
    }
