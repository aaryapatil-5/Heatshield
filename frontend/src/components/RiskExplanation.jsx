import React from 'react';
import { RISK_COLORS } from '../services/api';
import { AlertTriangle, ShieldCheck, HeartPulse, Sparkles, TrendingUp } from 'lucide-react';

export default function RiskExplanation({ snapshot, thermalMetric = 'heat_index' }) {
  if (!snapshot) {
    return <div className="panel empty-state">Select a location to inspect thermal risk.</div>;
  }

  const riskCat = snapshot.risk_category || 'LOW';
  const riskColor = RISK_COLORS[riskCat] || '#64748b';
  const probPct = Math.round((snapshot.risk_probability || 0) * 100);
  const confPct = Math.round((snapshot.confidence || 0) * 100);

  return (
    <div className="risk-explanation-panel">
      {/* Panel Header */}
      <div className="panel-header-row">
        <div>
          <div className="panel-title-wrap">
            <h2 className="panel-title">{snapshot.name}</h2>
            {snapshot.is_escalating && (
              <span className="escalation-pulse-badge">
                <TrendingUp className="w-3 h-3 mr-1" />
                Escalating Heatwave Demo
              </span>
            )}
          </div>
          <p className="panel-subtitle">
            {snapshot.district} · {snapshot.city}
          </p>
        </div>
        <div className="source-pill">{snapshot.data_status}</div>
      </div>

      {/* Main Risk Hero Card */}
      <div className="risk-hero-card" style={{ borderColor: `${riskColor}40` }}>
        <div className="risk-hero-gauge-box">
          <div className="risk-gauge-circle" style={{ borderColor: riskColor }}>
            <span className="risk-gauge-number" style={{ color: riskColor }}>
              {probPct}
            </span>
            <span className="risk-gauge-pct">%</span>
          </div>
        </div>

        <div className="risk-hero-meta">
          <div className="risk-category-tag-row">
            <span
              className="risk-hero-badge"
              style={{ backgroundColor: riskColor }}
            >
              {riskCat} RISK
            </span>
            <span className="risk-confidence-text">
              Model Confidence: {confPct}%
            </span>
          </div>
          <p className="risk-hero-summary">
            Projected localized human thermal risk based on compounding meteorological load and vulnerability.
          </p>
        </div>
      </div>

      {/* Health-Impact Risk Proxy */}
      <div className="health-proxy-card">
        <div className="health-proxy-header">
          <HeartPulse className="w-4 h-4 text-rose-400 mr-1.5" />
          <span className="health-proxy-title">{snapshot.health_risk_level || 'Health-Impact Risk Proxy'}</span>
        </div>
        <p className="health-proxy-desc">
          {snapshot.health_risk_description}
        </p>
        <p className="health-proxy-disclaimer">
          Environmental health-impact proxy. Does NOT predict clinical admissions or mortality numbers.
        </p>
      </div>

      {/* Why is this location at risk? (Explainability & Contributing Factors) */}
      <div className="drivers-section">
        <h3 className="section-heading">Why is this location at risk?</h3>
        <p className="section-subtext">
          Primary contributing factors identified by the AI ensemble model:
        </p>

        <div className="driver-list">
          {snapshot.risk_contributors && snapshot.risk_contributors.length > 0 ? (
            snapshot.risk_contributors.map((driver, idx) => (
              <div key={driver.factor || idx} className="driver-item">
                <span className="driver-rank">{idx + 1}</span>
                <div className="driver-info">
                  <div className="driver-label-row">
                    <span className="driver-name">{driver.factor}</span>
                    <span className="driver-pct">+{driver.contribution_pct}%</span>
                  </div>
                  <div className="driver-bar-track">
                    <div
                      className="driver-bar-fill"
                      style={{
                        width: `${Math.min(100, Math.max(8, driver.contribution_pct * 2.2))}%`,
                        backgroundColor: idx === 0 ? '#ef4444' : idx === 1 ? '#f97316' : '#3b82f6'
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-slate-400 text-xs">No dominant risk drivers detected for current baseline conditions.</p>
          )}
        </div>
      </div>

      {/* Multi-Metric Thermal Comparison Table */}
      <div className="thermal-compare-card">
        <div className="compare-header">
          <Sparkles className="w-3.5 h-3.5 text-orange-400 mr-1.5" />
          <span>Multi-Metric Thermal Comparison</span>
        </div>
        <div className="compare-grid">
          <div className="compare-cell">
            <span className="cell-label">Heat Index</span>
            <b className="cell-val">{snapshot.heat_index_c?.toFixed(1)}°C</b>
            <span className="cell-sub">{snapshot.heat_index_category}</span>
          </div>
          <div className="compare-cell">
            <span className="cell-label">WBGT Outdoor</span>
            <b className="cell-val">{snapshot.wbgt_outdoor_c?.toFixed(1)}°C</b>
            <span className="cell-sub">{snapshot.wbgt_outdoor_category}</span>
          </div>
          <div className="compare-cell">
            <span className="cell-label">WBGT Indoor</span>
            <b className="cell-val">{snapshot.wbgt_indoor_c?.toFixed(1)}°C</b>
            <span className="cell-sub">Shaded</span>
          </div>
          <div className="compare-cell">
            <span className="cell-label">UTCI (Fiala)</span>
            <b className="cell-val">{snapshot.utci_c?.toFixed(1)}°C</b>
            <span className="cell-sub">{snapshot.utci_category}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
