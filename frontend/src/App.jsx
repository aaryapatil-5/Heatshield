import React, { useEffect, useState, useCallback } from 'react';
import Header from './components/Header';
import StatCard from './components/StatCard';
import MapView from './components/MapView';
import RiskExplanation from './components/RiskExplanation';
import ForecastTimeline from './components/ForecastTimeline';
import VulnerabilityPanel from './components/VulnerabilityPanel';
import AlertFeed from './components/AlertFeed';
import RecommendationsPanel from './components/RecommendationsPanel';
import HistoricalTrends from './components/HistoricalTrends';
import SimulationSandbox from './components/SimulationSandbox';
import ModelTransparency from './components/ModelTransparency';
import { api, RISK_COLORS } from './services/api';
import { Thermometer, Droplets, Gauge, ShieldAlert, AlertTriangle, RefreshCw, CheckCircle2 } from 'lucide-react';

const CITIES = ['Mumbai', 'Delhi NCR', 'Ahmedabad'];

export default function App() {
  const [mode, setMode] = useState('demo');
  const [selectedCity, setSelectedCity] = useState('Mumbai');
  const [locations, setLocations] = useState([]);
  const [selectedLocationId, setSelectedLocationId] = useState('ward-dharavi');
  const [thermalMetric, setThermalMetric] = useState('heat_index');
  const [activeTab, setActiveTab] = useState('dashboard');

  const [snapshot, setSnapshot] = useState(null);
  const [forecastList, setForecastList] = useState([]);
  const [geoData, setGeoData] = useState(null);
  const [alertsList, setAlertsList] = useState([]);
  const [recsList, setRecsList] = useState([]);
  const [historyList, setHistoryList] = useState([]);
  const [perfData, setPerfData] = useState(null);

  const [loading, setLoading] = useState(true);
  const [switchingMode, setSwitchingMode] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [notification, setNotification] = useState('');

  // Initial load of locations list
  const loadLocations = useCallback(async (city) => {
    try {
      const locs = await api.getLocations(city);
      setLocations(locs);
      if (locs.length > 0) {
        // If current selected location is not in the new city, pick the first
        const exists = locs.some((l) => l.id === selectedLocationId);
        if (!exists) {
          setSelectedLocationId(locs[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load locations:', err);
    }
  }, [selectedLocationId]);

  // Load all intelligence data for current selection
  const loadData = useCallback(async (locId = selectedLocationId, metric = thermalMetric, city = selectedCity) => {
    setLoading(true);
    setErrorMsg('');
    try {
      const [snapRes, fcRes, mapRes, alertsRes, recsRes, histRes, perfRes, modeRes] =
        await Promise.all([
          api.getCurrentRisk(locId, metric),
          api.getForecast(locId, metric),
          api.getRiskMap(city, metric),
          api.getAlerts(locId, metric),
          api.getRecommendations(locId, metric),
          api.getHistory(locId),
          api.getModelPerformance(),
          api.getMode(),
        ]);

      setSnapshot(snapRes);
      setForecastList(fcRes.forecast || []);
      setGeoData(mapRes);
      setAlertsList(alertsRes.alerts || []);
      setRecsList(recsRes.recommendations || []);
      setHistoryList(histRes.history || []);
      setPerfData(perfRes);
      setMode(modeRes.mode || 'demo');
    } catch (err) {
      console.error('Error fetching dashboard intelligence:', err);
      setErrorMsg(
        'Unable to communicate with the HeatShield AI backend. Please verify FastAPI is running at http://localhost:8000.'
      );
    } finally {
      setLoading(false);
    }
  }, [selectedLocationId, thermalMetric, selectedCity]);

  // City change handler
  const handleSelectCity = (newCity) => {
    setSelectedCity(newCity);
    loadLocations(newCity);
  };

  // Location selector change handler
  const handleSelectLocation = (locId) => {
    setSelectedLocationId(locId);
  };

  // Metric selector change handler
  const handleSelectMetric = (metric) => {
    setThermalMetric(metric);
  };

  // Mode toggle handler
  const handleToggleMode = async () => {
    setSwitchingMode(true);
    const nextMode = mode === 'demo' ? 'live' : 'demo';
    try {
      await api.setMode(nextMode);
      setMode(nextMode);
      setNotification(`Switched to ${nextMode.toUpperCase()} Mode.`);
      setTimeout(() => setNotification(''), 4000);
      await loadData(selectedLocationId, thermalMetric, selectedCity);
    } catch (err) {
      console.error('Failed to toggle mode:', err);
      setErrorMsg('Could not switch data source mode.');
    } finally {
      setSwitchingMode(false);
    }
  };

  // Effects
  useEffect(() => {
    loadLocations(selectedCity);
  }, [selectedCity, loadLocations]);

  useEffect(() => {
    if (selectedLocationId) {
      loadData(selectedLocationId, thermalMetric, selectedCity);
    }
  }, [selectedLocationId, thermalMetric, selectedCity, loadData]);

  const metricName =
    thermalMetric === 'wbgt'
      ? 'WBGT Outdoor'
      : thermalMetric === 'utci'
      ? 'UTCI (Fiala)'
      : 'NOAA Heat Index';

  const currentThermalVal =
    thermalMetric === 'wbgt'
      ? snapshot?.wbgt_outdoor_c
      : thermalMetric === 'utci'
      ? snapshot?.utci_c
      : snapshot?.heat_index_c;

  const currentThermalCat =
    thermalMetric === 'wbgt'
      ? snapshot?.wbgt_outdoor_category
      : thermalMetric === 'utci'
      ? snapshot?.utci_category
      : snapshot?.heat_index_category;

  return (
    <div className="heatshield-app">
      {/* Primary Header */}
      <Header
        mode={mode}
        onToggleMode={handleToggleMode}
        cities={CITIES}
        selectedCity={selectedCity}
        onSelectCity={handleSelectCity}
        thermalMetric={thermalMetric}
        onSelectMetric={handleSelectMetric}
        activeTab={activeTab}
        onSelectTab={setActiveTab}
      />

      {/* Global Status & Location Toolbar */}
      <div className="status-toolbar">
        <div className="toolbar-left">
          <label className="toolbar-label">Active Monitoring Ward / Grid:</label>
          <select
            className="toolbar-select"
            value={selectedLocationId}
            onChange={(e) => handleSelectLocation(e.target.value)}
          >
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id}>
                {loc.name} · {loc.district} {loc.is_escalating ? '🔥 [Escalating Wave Demo]' : ''}
              </option>
            ))}
          </select>
        </div>

        <div className="toolbar-right">
          {notification && <span className="notification-pill">{notification}</span>}
          <div className="data-provenance-tag">
            <span className="dot"></span>
            <span>
              {mode === 'demo'
                ? 'DETERMINISTIC SIMULATION (SEED 26083)'
                : snapshot?.data_status === 'DEMO FALLBACK'
                ? 'DEMO FALLBACK (LIVE WEATHER UNREACHABLE)'
                : 'LIVE OPEN-METEO WEATHER OBSERVATIONS'}
            </span>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="dashboard-content">
        {errorMsg && (
          <div className="error-banner">
            <AlertTriangle className="w-5 h-5 text-amber-400 mr-2 flex-shrink-0" />
            <div className="flex-1">
              <b>System Notice:</b> {errorMsg}
            </div>
            <button className="retry-btn" onClick={() => loadData()}>
              <RefreshCw className="w-4 h-4 mr-1" /> Retry
            </button>
          </div>
        )}

        {loading ? (
          <div className="loading-state-box">
            <div className="pulse-spinner"></div>
            <p className="loading-text">Synthesizing localized heat intelligence & ML projections...</p>
          </div>
        ) : (
          <>
            {/* Top 4 Key Environmental & Risk Indicator Cards */}
            <section className="top-metrics-grid">
              <StatCard
                title="Air Temperature (2m)"
                value={snapshot?.temperature_c?.toFixed(1)}
                unit="°C"
                subtitle="Dry-bulb ambient temperature"
                icon={Thermometer}
              />
              <StatCard
                title="Relative Humidity"
                value={snapshot?.humidity_pct?.toFixed(0)}
                unit="%"
                subtitle="Moisture evaporative resistance"
                icon={Droplets}
              />
              <StatCard
                title={metricName}
                value={currentThermalVal?.toFixed(1)}
                unit="°C"
                subtitle="Physical apparent thermal stress"
                category={currentThermalCat}
                icon={Gauge}
              />
              <StatCard
                title="AI Heat Risk Severity"
                value={snapshot?.risk_category}
                probability={snapshot?.risk_probability}
                subtitle={`Confidence: ${Math.round((snapshot?.confidence || 0.8) * 100)}%`}
                category={snapshot?.risk_category}
                icon={ShieldAlert}
              />
            </section>

            {/* TAB 1: Situation Room (Overview, Map, Risk Hero, 5-Day preview, Alerts, Recs) */}
            {activeTab === 'dashboard' && (
              <>
                <section className="main-gis-grid">
                  <div className="map-column">
                    <MapView
                      geoData={geoData}
                      selectedLocationId={selectedLocationId}
                      onSelectLocation={handleSelectLocation}
                      currentCity={selectedCity}
                      thermalMetric={thermalMetric}
                    />
                  </div>
                  <div className="risk-column">
                    <RiskExplanation
                      snapshot={snapshot}
                      thermalMetric={thermalMetric}
                    />
                  </div>
                </section>

                <section className="dashboard-section-row">
                  <ForecastTimeline
                    forecastData={forecastList}
                    thermalMetric={thermalMetric}
                  />
                </section>

                <section className="dashboard-section-row">
                  <VulnerabilityPanel snapshot={snapshot} />
                </section>

                <section className="two-col-layout">
                  <AlertFeed alerts={alertsList} />
                  <RecommendationsPanel recommendationsList={recsList} />
                </section>
              </>
            )}

            {/* TAB 2: 5-Day Early Warning Deep Dive */}
            {activeTab === 'forecast' && (
              <div className="tab-page-container">
                <ForecastTimeline
                  forecastData={forecastList}
                  thermalMetric={thermalMetric}
                />
                <div className="mt-6">
                  <AlertFeed alerts={alertsList} />
                </div>
              </div>
            )}

            {/* TAB 3: Interactive What-If Simulation Sandbox */}
            {activeTab === 'simulate' && (
              <div className="tab-page-container">
                <SimulationSandbox
                  locationId={selectedLocationId}
                  locationName={snapshot?.name}
                  city={snapshot?.city}
                  thermalMetric={thermalMetric}
                />
              </div>
            )}

            {/* TAB 4: Historical Climatological Trends */}
            {activeTab === 'history' && (
              <div className="tab-page-container">
                <HistoricalTrends
                  historyData={historyList}
                  locationName={snapshot?.name}
                  city={snapshot?.city}
                />
              </div>
            )}

            {/* TAB 5: Model Transparency, Methodology & Validation */}
            {activeTab === 'transparency' && (
              <div className="tab-page-container">
                <ModelTransparency
                  perfData={perfData}
                  thermalMetric={thermalMetric}
                />
              </div>
            )}
          </>
        )}
      </main>

      {/* Official Prototype Boundary Footer */}
      <footer className="footer-bar">
        <div className="footer-content">
          <p className="footer-primary-text">
            <b>HeatShield AI</b> · Smart India Hackathon 2026 (PS ID SIH26083) · Ministry of Earth Sciences (MoES)
          </p>
          <p className="footer-disclaimer">
            Decision-support prototype demonstration. Does not replace official IMD heatwave forecasts or certified clinical medical advisories.
          </p>
        </div>
      </footer>
    </div>
  );
}
