import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { ShieldCheck, BookOpen, AlertOctagon, CheckCircle2, BarChart2, Cpu, Scale } from 'lucide-react';

export default function ModelTransparency({ perfData, thermalMetric = 'heat_index' }) {
  if (!perfData) {
    return <div className="panel empty-state">Loading model performance intelligence...</div>;
  }

  const metrics = perfData.metrics || {};
  const importances = perfData.feature_importances || {};

  // Format importances for Recharts bar chart
  const importanceChartData = Object.entries(importances).map(([k, v]) => {
    const labels = {
      heat_index_c: 'Thermal Stress Index',
      temperature_c: 'Air Temperature',
      vulnerability_score: 'Demographic Vulnerability',
      humidity_pct: 'Relative Humidity',
      exposure_score: 'Population Exposure',
      forecast_trend_c: 'Forecast Trend',
      solar_w_m2: 'Solar Radiation',
      heat_exposure_pct: 'Historical Heat Deficit',
      wind_kmh: 'Wind Speed'
    };
    return {
      feature: labels[k] || k,
      importance_pct: Math.round(v * 1000) / 10
    };
  }).sort((a, b) => b.importance_pct - a.importance_pct);

  return (
    <div className="panel transparency-panel">
      <div className="panel-header-row">
        <div>
          <div className="panel-title-wrap">
            <ShieldCheck className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">Model Transparency, Scientific Grounding & Validation</h2>
          </div>
          <p className="panel-subtitle">
            Complete architectural explainability, peer-reviewed thermal stress formulation, and backtesting metrics
          </p>
        </div>
        <span className="source-pill">SCIENTIFIC AUDIT TRAIL</span>
      </div>

      {/* Mandatory Validation Disclaimer Banner */}
      <div className="transparency-warning-banner">
        <AlertOctagon className="w-5 h-5 text-amber-400 mr-3 flex-shrink-0" />
        <div>
          <b className="text-amber-200">Scientific Validation Disclosure (MoES Prototype Protocol):</b>
          <p className="text-amber-100/90 text-xs mt-0.5">
            {perfData.official_disclaimer ||
              'Prototype validation on simulated/demo data. Real-world validation requires official historical datasets from IMD/MoES.'}
          </p>
        </div>
      </div>

      {/* 3-Layer Scientific Methodology Section */}
      <div className="methodology-grid">
        <div className="method-box">
          <div className="method-header">
            <Scale className="w-4 h-4 text-orange-400 mr-1.5" />
            <span className="method-title">Layer 1: Physical Thermal Stress</span>
          </div>
          <p className="method-desc">
            Rather than inventing an unverified formula, the system implements 3 established biometeorological frameworks:
          </p>
          <ul className="method-list">
            <li>
              <b>NOAA/NWS Heat Index:</b> Rothfusz 9-term polynomial regression modeling apparent temperature from 2m dry-bulb temperature and relative humidity.
            </li>
            <li>
              <b>ISO 7243 WBGT:</b> Stull (2011) psychrometric wet-bulb + Liljegren/BOM solar radiation black globe formulation for occupational manual labor limits.
            </li>
            <li>
              <b>ISB UTCI:</b> Operational 6th-order approximation of the human multi-node thermophysiological heat exchange model (Fiala et al.).
            </li>
          </ul>
        </div>

        <div className="method-box">
          <div className="method-header">
            <Cpu className="w-4 h-4 text-blue-400 mr-1.5" />
            <span className="method-title">Layer 2 & 3: Vulnerability & AI Ensemble</span>
          </div>
          <p className="method-desc">
            Interpretable AI model synthesizing physical climate hazards with local socioeconomic vulnerability:
          </p>
          <ul className="method-list">
            <li>
              <b>Modular Vulnerability:</b> Transparent composite score combining Census density, elderly share (&ge;60), outdoor labor %, impervious built-up surface %, and cooling center deficits.
            </li>
            <li>
              <b>Interpretable Ensemble Forest:</b> 80-tree Random Forest classifier predicting risk probability and confidence based on decision-boundary variance.
            </li>
            <li>
              <b>Health-Impact Proxy:</b> Maps compounding thermal-demographic stress into physiological risk categories without fabricating mortality counts.
            </li>
          </ul>
        </div>
      </div>

      {/* Validation Metrics Grid */}
      <div className="validation-section">
        <h3 className="section-heading">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 mr-1.5 inline" />
          Model Backtesting & Evaluation Metrics
        </h3>
        <p className="section-subtext">
          Temporal holdout split evaluation metrics (Test Cohort Size: {metrics.sample_size || 600} samples):
        </p>

        <div className="metrics-cards-row">
          <div className="metric-badge-box">
            <span className="m-label">Precision</span>
            <span className="m-value">{metrics.precision}</span>
            <span className="m-sub">Low false positives</span>
          </div>
          <div className="metric-badge-box">
            <span className="m-label">Recall</span>
            <span className="m-value">{metrics.recall}</span>
            <span className="m-sub">High heatwave capture</span>
          </div>
          <div className="metric-badge-box">
            <span className="m-label">F1-Score</span>
            <span className="m-value">{metrics.f1}</span>
            <span className="m-sub">Harmonic balance</span>
          </div>
          <div className="metric-badge-box">
            <span className="m-label">ROC-AUC</span>
            <span className="m-value">{metrics.roc_auc}</span>
            <span className="m-sub">Discrimination power</span>
          </div>
          <div className="metric-badge-box">
            <span className="m-label">Brier Score</span>
            <span className="m-value">{metrics.brier_score}</span>
            <span className="m-sub">Probability calibration</span>
          </div>
          <div className="metric-badge-box">
            <span className="m-label">False Alarm Rate</span>
            <span className="m-value">{metrics.false_alarm_rate}</span>
            <span className="m-sub">Type I error</span>
          </div>
          <div className="metric-badge-box">
            <span className="m-label">Missed Events</span>
            <span className="m-value">{metrics.missed_event_rate}</span>
            <span className="m-sub">Type II error</span>
          </div>
        </div>
      </div>

      {/* Global Feature Importances Chart */}
      <div className="feature-importances-wrap">
        <h3 className="section-heading">
          <BarChart2 className="w-4 h-4 text-orange-400 mr-1.5 inline" />
          Global Feature Importance Distribution (Ensemble Gini Gain)
        </h3>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart
              data={importanceChartData}
              layout="vertical"
              margin={{ top: 10, right: 30, left: 120, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
              <XAxis type="number" stroke="#94a3b8" fontSize={11} unit="%" />
              <YAxis
                type="category"
                dataKey="feature"
                stroke="#cbd5e1"
                fontSize={11}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '8px',
                  fontSize: '12px',
                  color: '#f8fafc'
                }}
                formatter={(val) => [`${val}%`, 'Relative Importance']}
              />
              <Bar dataKey="importance_pct" fill="#f97316" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
