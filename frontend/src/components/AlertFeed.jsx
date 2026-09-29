import React from 'react';
import { AlertTriangle, Bell, Clock, MapPin, CheckCircle2 } from 'lucide-react';

export default function AlertFeed({ alerts }) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="panel alerts-panel">
        <div className="panel-header-row">
          <div className="panel-title-wrap">
            <Bell className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">Active AI Alerts & Advisories</h2>
          </div>
        </div>
        <div className="alerts-empty-box">
          <CheckCircle2 className="w-8 h-8 text-emerald-400 mb-2" />
          <p className="text-sm font-semibold text-slate-200">No Severe Prototype Heat Alerts</p>
          <p className="text-xs text-slate-400 mt-1">
            Current and projected 48h thermal load remains within standard baseline thresholds.
          </p>
        </div>
      </div>
    );
  }

  const severityStyles = {
    EMERGENCY: {
      border: 'border-red-600',
      bg: 'bg-red-950/40',
      badgeBg: 'bg-red-600',
      badgeText: 'text-white'
    },
    WARNING: {
      border: 'border-orange-500',
      bg: 'bg-orange-950/40',
      badgeBg: 'bg-orange-500',
      badgeText: 'text-white'
    },
    ADVISORY: {
      border: 'border-amber-500',
      bg: 'bg-amber-950/30',
      badgeBg: 'bg-amber-500',
      badgeText: 'text-slate-950'
    }
  };

  return (
    <div className="panel alerts-panel">
      <div className="panel-header-row">
        <div>
          <div className="panel-title-wrap">
            <Bell className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">Active AI Early Warning Alerts</h2>
          </div>
          <p className="panel-subtitle">
            Automated operational notifications generated from compound thermal-stress and vulnerability thresholds
          </p>
        </div>
        <span className="alerts-count-badge">{alerts.length} Active Notice{alerts.length > 1 ? 's' : ''}</span>
      </div>

      <div className="alerts-stack">
        {alerts.map((alert, idx) => {
          const style = severityStyles[alert.severity] || severityStyles.ADVISORY;

          return (
            <div
              key={alert.id || idx}
              className={`alert-entry-card ${style.border} ${style.bg}`}
            >
              <div className="alert-top-bar">
                <div className="alert-badge-group">
                  <span className={`alert-severity-pill ${style.badgeBg} ${style.badgeText}`}>
                    {alert.severity}
                  </span>
                  <span className="alert-title-text">{alert.title}</span>
                </div>
                <div className="alert-time-tag">
                  <Clock className="w-3.5 h-3.5 mr-1" />
                  <span>{alert.valid_time}</span>
                </div>
              </div>

              <div className="alert-meta-row">
                <div className="meta-item">
                  <MapPin className="w-3.5 h-3.5 text-slate-400 mr-1" />
                  <span>{alert.affected_area}</span>
                </div>
                {alert.thermal_summary && (
                  <div className="meta-item font-mono text-orange-300">
                    {alert.thermal_summary}
                  </div>
                )}
              </div>

              <div className="alert-reason-block">
                <span className="reason-label">Contributing Factors:</span>
                <p className="reason-text">{alert.scientific_reason}</p>
              </div>

              <div className="alert-action-block">
                <span className="action-label">Recommended Action:</span>
                <p className="action-text">{alert.recommended_action}</p>
              </div>

              <div className="alert-disclaimer-tag">
                {alert.disclaimer || 'Prototype AI Alert — Decision Support Only — Not an Official IMD Bulletin'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
