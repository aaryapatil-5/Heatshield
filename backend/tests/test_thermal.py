import pytest
from app.thermal.heat_index import heat_index_c, heat_index_category, explain_heat_index
from app.thermal.wbgt import wbgt_c, wbgt_category, explain_wbgt, stull_wet_bulb_c
from app.thermal.utci import utci_approx_c, utci_category, explain_utci
from app.thermal.engine import get_active_thermal_stress, compute_all_thermal_metrics


def test_heat_index_known_warm_humid_case():
    """NOAA lookup test: 35°C at 60% RH produces apparent temperature around 44-48°C."""
    hi = heat_index_c(35.0, 60.0)
    assert 43.0 <= hi <= 49.0
    assert heat_index_category(hi) in {'VERY HIGH', 'EXTREME'}


def test_heat_index_mild_case():
    """At mild temperatures (e.g. 24°C), Heat Index should be low risk."""
    hi = heat_index_c(24.0, 50.0)
    assert hi < 27.0
    assert heat_index_category(hi) == 'LOW'


def test_heat_index_explanation_structure():
    exp = explain_heat_index(36.0, 65.0)
    assert exp['metric_name'] == 'NOAA / NWS Heat Index'
    assert 'input_variables' in exp
    assert 'physiological_impact' in exp


def test_wbgt_outdoor_vs_indoor():
    """Outdoor WBGT with strong solar radiation should exceed indoor WBGT."""
    wbgt_out = wbgt_c(temp_c=36.0, rh=55.0, wind_kmh=10.0, solar_w_m2=800.0, outdoor=True)
    wbgt_in = wbgt_c(temp_c=36.0, rh=55.0, wind_kmh=10.0, solar_w_m2=0.0, outdoor=False)
    assert wbgt_out > wbgt_in
    assert wbgt_category(wbgt_out) in {'HIGH', 'VERY HIGH', 'EXTREME'}


def test_stull_wet_bulb_bounds():
    tw = stull_wet_bulb_c(35.0, 60.0)
    # Wet bulb must be between dew point and dry bulb
    assert 20.0 <= tw <= 35.0


def test_utci_operational_bounds():
    utci = utci_approx_c(temp_c=38.0, rh=50.0, wind_kmh=8.0, solar_w_m2=750.0)
    assert 35.0 <= utci <= 55.0
    cat = utci_category(utci)
    assert cat in {'HIGH', 'VERY HIGH', 'EXTREME'}


def test_unified_thermal_engine():
    res = get_active_thermal_stress(35.0, 60.0, metric='wbgt')
    assert res['active_metric'] == 'wbgt'
    assert 'comparative' in res
    assert 'heat_index_c' in res['comparative']
    assert 'wbgt_outdoor_c' in res['comparative']
    assert 'utci_c' in res['comparative']
