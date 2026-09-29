import React from 'react';
import { ShieldAlert, Sun, Activity, Radio, Info } from 'lucide-react';

export default function Header({
  mode,
  onToggleMode,
  cities,
  selectedCity,
  onSelectCity,
  thermalMetric,
  onSelectMetric,
  activeTab,
  onSelectTab
}) {
  return (
    <header className="header-nav">
      <div className="header-container">
        {/* Brand & Organization Title */}
        <div className="header-brand-block">
          <div className="brand-logo-wrap">
            <div className="brand-icon-box">
              <ShieldAlert className="w-6 h-6 text-orange-400" />
            </div>
            <div>
              <div className="brand-title-row">
                <span className="brand-name">HeatShield</span>
                <span className="brand-ai-badge">AI</span>
                <span className="brand-sih-tag">MoES · SIH26083</span>
              </div>
              <p className="brand-subtitle">
                Extreme Heatwave Early Warning & Human Thermal Stress Intelligence
              </p>
            </div>
          </div>
        </div>

        {/* Global Controls: City, Metric, Mode Toggle */}
        <div className="header-controls">
          {/* City / Region Selector */}
          <div className="control-group">
            <label className="control-label">Region / City</label>
            <select
              className="select-input"
              value={selectedCity}
              onChange={(e) => onSelectCity(e.target.value)}
            >
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Thermal Metric Selector */}
          <div className="control-group">
            <label className="control-label">Thermal Index Metric</label>
            <div className="metric-pill-group">
              <button
                type="button"
                className={`metric-pill ${thermalMetric === 'heat_index' ? 'active' : ''}`}
                onClick={() => onSelectMetric('heat_index')}
                title="NOAA/NWS Heat Index (Temp + Humidity)"
              >
                Heat Index
              </button>
              <button
                type="button"
                className={`metric-pill ${thermalMetric === 'wbgt' ? 'active' : ''}`}
                onClick={() => onSelectMetric('wbgt')}
                title="Wet Bulb Globe Temperature (Temp + Humidity + Wind + Solar)"
              >
                WBGT
              </button>
              <button
                type="button"
                className={`metric-pill ${thermalMetric === 'utci' ? 'active' : ''}`}
                onClick={() => onSelectMetric('utci')}
                title="Universal Thermal Climate Index (Fiala Multinode Biometeorology)"
              >
                UTCI
              </button>
            </div>
          </div>

          {/* Live vs Demo Mode Toggle */}
          <div className="control-group">
            <label className="control-label">Data Source Mode</label>
            <button
              type="button"
              className={`mode-toggle-btn ${mode === 'live' ? 'live-active' : 'demo-active'}`}
              onClick={onToggleMode}
              title={
                mode === 'live'
                  ? 'Active Live Mode: Querying Open-Meteo API. Click to switch to Demo Mode.'
                  : 'Active Demo Mode: Using deterministic simulated dataset (seed 26083). Click to test Live Mode.'
              }
            >
              <span className="status-dot"></span>
              <span className="mode-btn-text">
                {mode === 'live' ? 'Live Weather API' : 'Demo / Simulated'}
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* Primary Section Navigation Tabs */}
      <nav className="header-tabs">
        <div className="tab-container">
          <button
            className={`tab-btn ${activeTab === 'dashboard' ? 'tab-active' : ''}`}
            onClick={() => onSelectTab('dashboard')}
          >
            <Activity className="w-4 h-4 mr-1.5" />
            Situation Room
          </button>
          <button
            className={`tab-btn ${activeTab === 'forecast' ? 'tab-active' : ''}`}
            onClick={() => onSelectTab('forecast')}
          >
            <Sun className="w-4 h-4 mr-1.5" />
            5-Day Early Warning
          </button>
          <button
            className={`tab-btn ${activeTab === 'simulate' ? 'tab-active' : ''}`}
            onClick={() => onSelectTab('simulate')}
          >
            <Radio className="w-4 h-4 mr-1.5" />
            What-If Simulator
          </button>
          <button
            className={`tab-btn ${activeTab === 'history' ? 'tab-active' : ''}`}
            onClick={() => onSelectTab('history')}
          >
            <Activity className="w-4 h-4 mr-1.5" />
            Historical Trends
          </button>
          <button
            className={`tab-btn ${activeTab === 'transparency' ? 'tab-active' : ''}`}
            onClick={() => onSelectTab('transparency')}
          >
            <Info className="w-4 h-4 mr-1.5" />
            Scientific Methodology & Validation
          </button>
        </div>
      </nav>
    </header>
  );
}
