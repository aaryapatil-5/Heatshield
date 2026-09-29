import sys
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_mode_get_and_set():
    r = client.get('/api/mode')
    assert r.status_code == 200
    assert 'mode' in r.json()

    # Switch to demo
    r_post = client.post('/api/mode', json={'mode': 'demo'})
    assert r_post.status_code == 200
    assert r_post.json()['mode'] == 'demo'


def test_thermal_metrics_catalog():
    r = client.get('/api/thermal-metrics')
    assert r.status_code == 200
    metrics = r.json()['metrics']
    assert 'heat_index' in metrics
    assert 'wbgt' in metrics
    assert 'utci' in metrics


def test_locations_list_and_city_filtering():
    r = client.get('/api/locations')
    assert r.status_code == 200
    all_locs = r.json()
    assert len(all_locs) >= 8

    r_mumbai = client.get('/api/locations?city=Mumbai')
    assert r_mumbai.status_code == 200
    assert all(l['city'] == 'Mumbai' for l in r_mumbai.json())


def test_current_risk_with_wbgt():
    r = client.get('/api/current-risk?location=ward-dharavi&metric=wbgt')
    assert r.status_code == 200
    data = r.json()
    assert data['id'] == 'ward-dharavi'
    assert 'wbgt_outdoor_c' in data
    assert 'risk_category' in data
    assert 'health_risk_level' in data
    assert 'risk_contributors' in data


def test_forecast_escalating_heatwave():
    r = client.get('/api/forecast?location=ward-dharavi')
    assert r.status_code == 200
    fc = r.json()['forecast']
    assert len(fc) == 5
    # Dharavi is escalating demo, so later days should have higher temps
    assert fc[-1]['temperature_c'] >= fc[0]['temperature_c']


def test_risk_map_geojson():
    r = client.get('/api/risk-map')
    assert r.status_code == 200
    geo = r.json()
    assert geo['type'] == 'FeatureCollection'
    assert len(geo['features']) >= 8
    first_feat = geo['features'][0]
    assert 'geometry' in first_feat
    assert 'properties' in first_feat
    assert 'risk_category' in first_feat['properties']


def test_alerts_and_recommendations():
    r_alerts = client.get('/api/alerts?location=ward-dharavi')
    assert r_alerts.status_code == 200
    assert 'alerts' in r_alerts.json()

    r_recs = client.get('/api/recommendations?location=ward-dharavi')
    assert r_recs.status_code == 200
    recs = r_recs.json()['recommendations']
    assert len(recs) >= 3


def test_model_performance():
    r = client.get('/api/model-performance')
    assert r.status_code == 200
    data = r.json()
    assert 'metrics' in data
    assert 'precision' in data['metrics']
    assert 'roc_auc' in data['metrics']
    assert 'feature_importances' in data


def test_predict_endpoint():
    payload = {
        'temperature_c': 38.5,
        'humidity_pct': 60.0,
        'wind_kmh': 12.0,
        'solar_w_m2': 700.0,
        'forecast_trend_c': 0.8,
        'vulnerability_score': 65.0,
        'exposure_score': 70.0,
        'heat_exposure_pct': 60.0
    }
    r = client.post('/api/predict', json=payload)
    assert r.status_code == 200
    out = r.json()
    assert 0.0 <= out['risk_probability'] <= 1.0
    assert out['risk_category'] in {'LOW', 'MODERATE', 'HIGH', 'VERY HIGH', 'EXTREME'}


def test_simulate_sandbox():
    payload = {
        'location_id': 'ward-dharavi',
        'delta_temperature_c': -1.5,
        'delta_green_cover_pct': 25.0,
        'added_cooling_centers': 8,
        'metric': 'heat_index'
    }
    r = client.post('/api/simulate', json=payload)
    assert r.status_code == 200
    sim = r.json()['simulation']
    assert 'baseline' in sim
    assert 'simulated' in sim
    assert 'impact' in sim
    # Increasing green cover and adding cooling centers should reduce risk
    assert sim['simulated']['risk_probability'] <= sim['baseline']['risk_probability']
