import pytest
from app.risk.classifier import predict, risk_contributors, BUNDLE


def test_model_trained_and_metrics_present():
    assert BUNDLE.model is not None
    assert 'f1' in BUNDLE.metrics
    assert 'roc_auc' in BUNDLE.metrics
    assert BUNDLE.metrics['f1'] > 0.65
    assert BUNDLE.metrics['roc_auc'] > 0.70


def test_predict_schema_and_ranges():
    features = {
        'temperature_c': 41.5,
        'humidity_pct': 65.0,
        'wind_kmh': 8.0,
        'solar_w_m2': 750.0,
        'heat_index_c': 52.0,
        'forecast_trend_c': 1.2,
        'vulnerability_score': 78.0,
        'exposure_score': 82.0,
        'heat_exposure_pct': 75.0
    }
    pred = predict(features)
    assert 0.0 <= pred['risk_probability'] <= 1.0
    assert pred['risk_category'] in {'LOW', 'MODERATE', 'HIGH', 'VERY HIGH', 'EXTREME'}
    assert 0.50 <= pred['confidence'] <= 0.99
    assert 'health_risk_level' in pred
    assert 'health_risk_description' in pred


def test_risk_contributors_breakdown():
    features = {
        'temperature_c': 42.0,
        'humidity_pct': 70.0,
        'wind_kmh': 6.0,
        'solar_w_m2': 800.0,
        'heat_index_c': 55.0,
        'forecast_trend_c': 1.5,
        'vulnerability_score': 85.0,
        'exposure_score': 80.0,
        'heat_exposure_pct': 80.0
    }
    drivers = risk_contributors(features)
    assert len(drivers) == 5
    total_pct = sum(d['contribution_pct'] for d in drivers)
    # Top 5 should account for the vast majority of relative weights
    assert 60.0 <= total_pct <= 100.0
