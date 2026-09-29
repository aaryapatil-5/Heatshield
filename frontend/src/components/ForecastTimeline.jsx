import React, { useState } from 'react';
import { AreaChart, Area, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from 'recharts';
import { RISK_COLORS } from '../services/api';
import { Calendar, AlertCircle, Wind, Droplets, ArrowUpRight } from 'lucide-react';

export default function ForecastTimeline({ forecastData, thermalMetric = 'heat_index' }) {
  const [selectedDayIndex, setSelectedDayIndex] = useState(0);

  if (!forecastData || forecastData.length === 0) {
    return <div className="panel empty-state">No forecast data available for selected location.</div>;
  }

  const selectedDay = forecastData[selectedDayIndex] || forecastData[0];

  const metricLabel =
    thermalMetric === 'wbgt' ? 'WBGT Outdoor' : thermalMetric === 'utci' ? 'UTCI' : 'Heat Index';

  return (
    <div className="forecast-panel">
      <div className="forecast-panel-header">
        <div>
          <div className="panel-title-wrap">
            <Calendar className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">5-Day Heatwave Early Warning & Risk Trajectory</h2>
          </div>
          <p className="panel-subtitle">
            Localized thermal stress progression combining meteorological forecasts and demographic vulnerability
          </p>
        </div>
        <div className="metric-tag-pill">Tracking: {metricLabel}</div>
      </div>

      {/* 5-Day Card Grid */}
      <div className="forecast-cards-grid">
        {forecastData.map((day, idx) => {
          const isSelected = idx === selectedDayIndex;
          const riskCat = day.risk_category || 'MODERATE';
          const badgeColor = RISK_COLORS[riskCat] || '#64748b';

          return (
            <div
              key={day.date || idx}
              className={`forecast-day-card ${isSelected ? 'selected' : ''}`}
              onClick={() => setSelectedDayIndex(idx)}
            >
              <div className="card-top-row">
                <span className="day-name">{idx === 0 ? 'Tomorrow' : day.day_label}</span>
                <span className="day-date">{day.date}</span>
              </div>

              <div className="card-temp-row">
                <span className="day-temp">{day.temperature_c?.toFixed(1)}°C</span>
                <span className="day-thermal-val">
                  {metricLabel.split(' ')[0]}: {day.thermal_index_c?.toFixed(1)}°C
                </span>
              </div>

              <div className="card-env-row">
                <span className="env-pill">
                  <Droplets className="w-3 h-3 mr-0.5 inline" /> {day.humidity_pct?.toFixed(0)}%
                </span>
                <span className="env-pill">
                  <Wind className="w-3 h-3 mr-0.5 inline" /> {day.wind_kmh?.toFixed(0)} km/h
                </span>
              </div>

              <div className="card-risk-badge-wrap">
                <span className="risk-pill" style={{ backgroundColor: badgeColor }}>
                  {riskCat}
                </span>
                <span className="conf-pill">
                  {Math.round((day.confidence || 0.75) * 100)}% conf.
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Trajectory Area & Line Chart */}
      <div className="forecast-chart-container">
        <div className="chart-header-row">
          <span className="chart-title">Thermal Index & Ambient Temperature Trajectory</span>
          <div className="chart-legend-custom">
            <span className="legend-indicator orange"></span>
            <span className="mr-3 text-xs text-slate-300">{metricLabel} (°C)</span>
            <span className="legend-indicator blue"></span>
            <span className="text-xs text-slate-300">Air Temp (°C)</span>
          </div>
        </div>

        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={230}>
            <AreaChart data={forecastData} margin={{ top: 10, right: 20, left: -15, bottom: 0 }}>
              <defs>
                <linearGradient id="thermalGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#f97316" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="tempGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#38bdf8" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
              <XAxis dataKey="day_label" stroke="#94a3b8" fontSize={11} tickLine={false} />
              <YAxis stroke="#94a3b8" fontSize={11} domain={['dataMin - 3', 'dataMax + 4']} tickLine={false} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '8px',
                  fontSize: '12px',
                  color: '#f8fafc'
                }}
              />
              <ReferenceLine y={40} stroke="#ef4444" strokeDasharray="4 4" label={{ value: 'IMD Extreme Threshold (40°C)', fill: '#ef4444', fontSize: 10 }} />
              <Area type="monotone" dataKey="thermal_index_c" name={metricLabel} stroke="#f97316" strokeWidth={2.5} fillOpacity={1} fill="url(#thermalGrad)" />
              <Line type="monotone" dataKey="temperature_c" name="Air Temperature" stroke="#38bdf8" strokeWidth={2} dot={{ r: 3 }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Selected Day Inspector */}
      {selectedDay && (
        <div className="forecast-selected-detail">
          <div className="detail-header">
            <span className="detail-title">
              Detailed Intelligence for {selectedDay.day_label} ({selectedDay.date})
            </span>
            <span
              className="detail-risk-badge"
              style={{ backgroundColor: RISK_COLORS[selectedDay.risk_category] || '#64748b' }}
            >
              {selectedDay.risk_category} Risk
            </span>
          </div>

          <div className="detail-grid">
            <div className="detail-item">
              <span className="detail-lbl">Air Temp</span>
              <b className="detail-val">{selectedDay.temperature_c?.toFixed(1)}°C</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">{metricLabel}</span>
              <b className="detail-val">{selectedDay.thermal_index_c?.toFixed(1)}°C</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">Humidity</span>
              <b className="detail-val">{selectedDay.humidity_pct?.toFixed(0)}%</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">Wind Speed</span>
              <b className="detail-val">{selectedDay.wind_kmh?.toFixed(0)} km/h</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">Solar Radiation</span>
              <b className="detail-val">{selectedDay.solar_w_m2?.toFixed(0)} W/m²</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">Risk Probability</span>
              <b className="detail-val">{Math.round((selectedDay.risk_probability || 0) * 100)}%</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">Model Confidence</span>
              <b className="detail-val">{Math.round((selectedDay.confidence || 0) * 100)}%</b>
            </div>
            <div className="detail-item">
              <span className="detail-lbl">Health Impact</span>
              <b className="detail-val text-xs text-rose-300" style={{ fontSize: '11px', marginTop: '2px' }}>
                {selectedDay.health_risk_level || 'Elevated Stress'}
              </b>
            </div>
          </div>

          {selectedDay.risk_contributors && selectedDay.risk_contributors.length > 0 && (
            <div className="detail-drivers-row">
              <span className="detail-drivers-lbl">Projected Risk Drivers:</span>
              <div className="detail-drivers-tags">
                {selectedDay.risk_contributors.slice(0, 3).map((d) => (
                  <span key={d.factor} className="driver-tag">
                    {d.factor} (+{d.contribution_pct}%)
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
