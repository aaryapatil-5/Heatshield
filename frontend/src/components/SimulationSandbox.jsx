import React, { useState, useEffect, useCallback } from 'react';
import { api, RISK_COLORS } from '../services/api';
import { Sliders, Sparkles, TrendingDown, TrendingUp, RefreshCw, ShieldAlert, Trees, Building2, Droplets, Sun } from 'lucide-react';

export default function SimulationSandbox({ locationId, locationName, city, thermalMetric = 'heat_index' }) {
  const [deltaTemp, setDeltaTemp] = useState(0.0);
  const [deltaHumidity, setDeltaHumidity] = useState(0.0);
  const [deltaGreen, setDeltaGreen] = useState(25.0);
  const [coolingCenters, setCoolingCenters] = useState(6);
  const [simResult, setSimResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const executeSimulation = useCallback(async (t, h, g, c, loc, met) => {
    setLoading(true);
    setError('');
    try {
      const res = await api.runSimulation({
        location_id: loc,
        delta_temperature_c: parseFloat(t),
        delta_humidity_pct: parseFloat(h),
        delta_green_cover_pct: parseFloat(g),
        added_cooling_centers: parseInt(c, 10),
        metric: met
      });
      setSimResult(res.simulation);
    } catch (err) {
      setError(err.message || 'Simulation execution failed.');
    } finally {
      setLoading(false);
    }
  }, []);

  // Automatic real-time recalculation on slider change with smooth 120ms debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      executeSimulation(deltaTemp, deltaHumidity, deltaGreen, coolingCenters, locationId, thermalMetric);
    }, 120);
    return () => clearTimeout(timer);
  }, [deltaTemp, deltaHumidity, deltaGreen, coolingCenters, locationId, thermalMetric, executeSimulation]);

  const handleSimulate = () => {
    executeSimulation(deltaTemp, deltaHumidity, deltaGreen, coolingCenters, locationId, thermalMetric);
  };

  const handleReset = () => {
    setDeltaTemp(0.0);
    setDeltaHumidity(0.0);
    setDeltaGreen(0.0);
    setCoolingCenters(0);
    executeSimulation(0.0, 0.0, 0.0, 0, locationId, thermalMetric);
  };

  return (
    <div className="panel simulation-panel">
      <div className="panel-header-row">
        <div>
          <div className="panel-title-wrap">
            <Sliders className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">Interactive Resilience & Climate Simulation Sandbox</h2>
          </div>
          <p className="panel-subtitle">
            Model counterfactual heatwave escalation vs urban cooling mitigation for {locationName} ({city})
          </p>
        </div>
        <span className="source-pill">WHAT-IF SCENARIO ENGINE</span>
      </div>

      <div className="sim-layout-grid">
        {/* Left: Interactive Controls */}
        <div className="sim-controls-box">
          <h3 className="sim-box-title">Scenario Parameters & Interventions</h3>

          {/* Air Temperature Shift */}
          <div className="sim-slider-group">
            <div className="slider-label-row">
              <span className="slider-label">
                <Sun className="w-3.5 h-3.5 text-amber-400 mr-1.5 inline" />
                Temperature Shift (Climate / Peak Wave)
              </span>
              <span className="slider-val-tag">
                {deltaTemp > 0 ? `+${deltaTemp}` : deltaTemp}°C
              </span>
            </div>
            <input
              type="range"
              min="-3.0"
              max="6.0"
              step="0.5"
              value={deltaTemp}
              onChange={(e) => setDeltaTemp(parseFloat(e.target.value))}
              className="range-input"
            />
            <div className="slider-range-ticks">
              <span>-3°C</span>
              <span>Baseline (0°C)</span>
              <span>+6°C (Extreme)</span>
            </div>
          </div>

          {/* Humidity Shift */}
          <div className="sim-slider-group">
            <div className="slider-label-row">
              <span className="slider-label">
                <Droplets className="w-3.5 h-3.5 text-cyan-400 mr-1.5 inline" />
                Relative Humidity Shift
              </span>
              <span className="slider-val-tag">
                {deltaHumidity > 0 ? `+${deltaHumidity}` : deltaHumidity}%
              </span>
            </div>
            <input
              type="range"
              min="-20"
              max="25"
              step="1"
              value={deltaHumidity}
              onChange={(e) => setDeltaHumidity(parseFloat(e.target.value))}
              className="range-input"
            />
            <div className="slider-range-ticks">
              <span>-20% (Dry)</span>
              <span>Baseline (0%)</span>
              <span>+25% (Sultry)</span>
            </div>
          </div>

          {/* Green Cover & Cool Roofs */}
          <div className="sim-slider-group">
            <div className="slider-label-row">
              <span className="slider-label">
                <Trees className="w-3.5 h-3.5 text-emerald-400 mr-1.5 inline" />
                Urban Canopy / Cool Roofs Expansion
              </span>
              <span className="slider-val-tag">+{deltaGreen}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="40"
              step="5"
              value={deltaGreen}
              onChange={(e) => setDeltaGreen(parseFloat(e.target.value))}
              className="range-input"
            />
            <div className="slider-range-ticks">
              <span>0% (No change)</span>
              <span>+20%</span>
              <span>+40% (Target Plan)</span>
            </div>
          </div>

          {/* Emergency Cooling Centers */}
          <div className="sim-slider-group">
            <div className="slider-label-row">
              <span className="slider-label">
                <Building2 className="w-3.5 h-3.5 text-indigo-400 mr-1.5 inline" />
                Deploy Emergency Cooling Centers
              </span>
              <span className="slider-val-tag">+{coolingCenters} Centers</span>
            </div>
            <input
              type="range"
              min="0"
              max="15"
              step="1"
              value={coolingCenters}
              onChange={(e) => setCoolingCenters(parseInt(e.target.value, 10))}
              className="range-input"
            />
            <div className="slider-range-ticks">
              <span>0 (Current)</span>
              <span>+8 Centers</span>
              <span>+15 Centers</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="sim-btn-row">
            <button
              type="button"
              className="sim-run-btn"
              onClick={handleSimulate}
              disabled={loading}
            >
              <Sparkles className="w-4 h-4 mr-1.5" />
              {loading ? 'Computing Scenarios...' : 'Run Simulation'}
            </button>
            <button
              type="button"
              className="sim-reset-btn"
              onClick={handleReset}
              disabled={loading}
            >
              <RefreshCw className="w-3.5 h-3.5 mr-1" />
              Reset
            </button>
          </div>

          {error && <div className="sim-error-alert">{error}</div>}
        </div>

        {/* Right: Simulation Comparative Results */}
        <div className="sim-results-box">
          <h3 className="sim-box-title">Counterfactual Model Assessment</h3>

          {simResult ? (
            <div className="sim-results-content">
              {/* Risk Delta Banner */}
              <div
                className={`sim-delta-banner ${
                  simResult.impact.net_direction === 'reduced'
                    ? 'reduced'
                    : simResult.impact.net_direction === 'increased'
                    ? 'increased'
                    : 'neutral'
                }`}
              >
                <div className="delta-icon-box">
                  {simResult.impact.net_direction === 'reduced' ? (
                    <TrendingDown className="w-6 h-6 text-emerald-400" />
                  ) : (
                    <TrendingUp className="w-6 h-6 text-rose-400" />
                  )}
                </div>
                <div>
                  <div className="delta-title">
                    {simResult.impact.net_direction === 'reduced'
                      ? 'Heat-Risk Mitigated'
                      : 'Elevated Risk Hazard'}
                  </div>
                  <div className="delta-desc">{simResult.impact.summary}</div>
                </div>
              </div>

              {/* Side-by-Side Comparison */}
              <div className="sim-compare-grid">
                <div className="sim-col baseline">
                  <span className="col-tag">Baseline State</span>
                  <div className="col-val-row">
                    <span className="col-big-val">
                      {Math.round(simResult.baseline.risk_probability * 100)}%
                    </span>
                    <span
                      className="col-badge"
                      style={{
                        backgroundColor:
                          RISK_COLORS[simResult.baseline.risk_category] || '#64748b'
                      }}
                    >
                      {simResult.baseline.risk_category}
                    </span>
                  </div>
                  <div className="col-details">
                    <div>Temp: <b>{simResult.baseline.temperature_c}°C</b></div>
                    <div>Humidity: <b>{simResult.baseline.humidity_pct}%</b></div>
                    <div>Green Canopy: <b>{simResult.baseline.green_cover_pct}%</b></div>
                  </div>
                </div>

                <div className="sim-col counterfactual">
                  <span className="col-tag">Simulated State</span>
                  <div className="col-val-row">
                    <span className="col-big-val">
                      {Math.round(simResult.simulated.risk_probability * 100)}%
                    </span>
                    <span
                      className="col-badge"
                      style={{
                        backgroundColor:
                          RISK_COLORS[simResult.simulated.risk_category] || '#64748b'
                      }}
                    >
                      {simResult.simulated.risk_category}
                    </span>
                  </div>
                  <div className="col-details">
                    <div>Sim Temp: <b>{simResult.simulated.temperature_c}°C</b></div>
                    <div>Sim Humidity: <b>{simResult.simulated.humidity_pct}%</b></div>
                    <div>Sim Green: <b>{simResult.simulated.green_cover_pct}%</b></div>
                    <div>Vulnerability: <b>{simResult.simulated.vulnerability_score}/100</b></div>
                  </div>
                </div>
              </div>

              {/* Health Impact Narrative */}
              <div className="sim-health-box">
                <span className="sim-health-title">Projected Physiological Health Shift:</span>
                <p className="sim-health-text">{simResult.simulated.health_risk_level}</p>
              </div>
            </div>
          ) : (
            <div className="sim-empty-prompt">
              <Sparkles className="w-10 h-10 text-slate-500 mb-3" />
              <p className="font-semibold text-slate-300">Ready for Counterfactual Analysis</p>
              <p className="text-xs text-slate-400 max-w-sm text-center mt-1">
                Adjust sliders to test climate escalation or urban cooling interventions (canopy, cooling shelters), then click <b>Run Simulation</b>.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
