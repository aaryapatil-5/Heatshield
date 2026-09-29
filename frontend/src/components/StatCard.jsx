import React from 'react';
import { RISK_COLORS } from '../services/api';

export default function StatCard({
  title,
  value,
  unit,
  subtitle,
  category,
  probability,
  badgeText,
  icon: Icon,
  variant = 'default'
}) {
  const badgeColor = category ? RISK_COLORS[category] || '#64748b' : '#3b82f6';

  return (
    <div className={`stat-card ${variant}`}>
      <div className="stat-card-header">
        <span className="stat-card-title">{title}</span>
        {Icon && <Icon className="w-4 h-4 text-slate-400" />}
      </div>

      <div className="stat-card-body">
        <div className="stat-card-value-row">
          <span className="stat-card-value">{value}</span>
          {unit && <span className="stat-card-unit">{unit}</span>}
        </div>

        {category && (
          <div className="stat-card-badge-row">
            <span
              className="stat-badge"
              style={{ backgroundColor: badgeColor }}
            >
              {category}
            </span>
            {probability !== undefined && (
              <span className="stat-prob-text">
                {Math.round(probability * 100)}% risk probability
              </span>
            )}
          </div>
        )}

        {badgeText && !category && (
          <div className="stat-card-badge-row">
            <span className="stat-badge-neutral">{badgeText}</span>
          </div>
        )}
      </div>

      {subtitle && <div className="stat-card-footer">{subtitle}</div>}
    </div>
  );
}
