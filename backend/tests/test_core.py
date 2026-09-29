import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.thermal.heat_index import heat_index_c, heat_index_category
from app.vulnerability.score import vulnerability_score, exposure_score
from app.risk.classifier import predict


def test_heat_index_known_warm_humid_case():
    hi=heat_index_c(35,60)
    assert 42 < hi < 50
    assert heat_index_category(hi) in {'VERY HIGH','EXTREME'}

def test_vulnerability_bounds():
    assert 0 <= vulnerability_score(40000,12,35,90,10,80) <= 100
    assert 0 <= exposure_score(40000,90) <= 100

def test_risk_prediction_schema():
    out=predict({'temperature_c':39,'humidity_pct':70,'wind_kmh':6,'heat_index_c':54,'forecast_trend_c':2,'vulnerability_score':80,'exposure_score':80,'heat_exposure_pct':80})
    assert 0 <= out['risk_probability'] <= 1
    assert out['risk_category'] in {'LOW','MODERATE','HIGH','VERY HIGH','EXTREME'}

def test_missing_api_keys_do_not_affect_demo_logic():
    from app.services.demo_data import location_snapshot, LOCATIONS
    snap=location_snapshot(LOCATIONS[0])
    assert snap['data_status'].startswith('DEMO')
