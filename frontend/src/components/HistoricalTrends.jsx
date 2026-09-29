import React, { useMemo } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';
import { History, Flame, CalendarDays, TrendingUp, AlertTriangle } from 'lucide-react';

export default function HistoricalTrends({ historyData, locationName, city }) {
  if (!historyData || historyData.length === 0) {
    return <div className="panel empty-state">No historical records available for this location.</div>;
  }

  // Sample data points to ensure smooth rendering
  const sampledHistory = useMemo(() => {
    return historyData.filter((_, i) => i % 2 === 0);
  }, [historyData]);

  // Compute key historical metrics
  const totalDays = historyData.length;
  const highRiskDays = historyData.filter((d) => d.high_risk).length;
  const maxTemp = Math.max(...historyData.map((d) => d.temperature_c));
  const maxHI = Math.max(...historyData.map((d) => d.heat_index_c));
  const avgTemp = (historyData.reduce((acc, d) => acc + d.temperature_c, 0) / totalDays).toFixed(1);

  return (
    <div className="panel historical-panel">
      <div className="panel-header-row">
        <div>
          <div className="panel-title-wrap">
            <History className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">Historical Heat Signal & Climatological Trend</h2>
          </div>
          <p className="panel-subtitle">
            90-day longitudinal thermal stress observations and heatwave event frequency for {locationName} ({city})
          </p>
        </div>
        <span className="source-pill">SIMULATED / DETERMINISTIC ARCHIVE</span>
      </div>

      {/* Historical Summary Cards */}
      <div className="historical-stats-grid">
        <div className="hist-stat-card">
          <span className="hist-stat-lbl">High-Risk Heat Days</span>
          <div className="hist-stat-val text-rose-400">
            <Flame className="w-5 h-5 mr-1.5 inline" />
            <span>{highRiskDays}</span>
            <small className="text-xs text-slate-400 ml-1">/ {totalDays} days</small>
          </div>
          <span className="hist-stat-desc">Heat Index &ge; 41°C or Temp &ge; 40°C</span>
        </div>

        <div className="hist-stat-card">
          <span className="hist-stat-lbl">Peak Historical Temp</span>
          <div className="hist-stat-val text-orange-400">
            <span>{maxTemp.toFixed(1)}°C</span>
          </div>
          <span className="hist-stat-desc">Peak ambient 2m temperature</span>
        </div>

        <div className="hist-stat-card">
          <span className="hist-stat-lbl">Peak Historical Heat Index</span>
          <div className="hist-stat-val text-red-500">
            <span>{maxHI.toFixed(1)}°C</span>
          </div>
          <span className="hist-stat-desc">Maximum apparent thermal load</span>
        </div>

        <div className="hist-stat-card">
          <span className="hist-stat-lbl">Seasonal Mean Temp</span>
          <div className="hist-stat-val text-slate-200">
            <span>{avgTemp}°C</span>
          </div>
          <span className="hist-stat-desc">Baseline regional thermal level</span>
        </div>
      </div>

      {/* 90-Day Trend Chart */}
      <div className="hist-chart-wrap">
        <div className="chart-header-row">
          <span className="chart-title">90-Day Apparent Heat Index vs Air Temperature</span>
          <div className="chart-legend-custom">
            <span className="legend-indicator orange"></span>
            <span className="mr-3 text-xs text-slate-300">Heat Index (°C)</span>
            <span className="legend-indicator blue"></span>
            <span className="text-xs text-slate-300">Air Temp (°C)</span>
          </div>
        </div>

        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={sampledHistory} margin={{ top: 10, right: 20, left: -15, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={10} tickLine={false} />
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
              <ReferenceLine y={40} stroke="#ef4444" strokeDasharray="4 4" label={{ value: 'Heatwave (40°C)', fill: '#ef4444', fontSize: 10 }} />
              <Line type="monotone" dataKey="heat_index_c" name="Heat Index" stroke="#f97316" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="temperature_c" name="Air Temperature" stroke="#38bdf8" strokeWidth={1.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="hist-note">
        <b>Methodological Grounding:</b> The 90-day trend models seasonal summer sinusoidal oscillations combined with urban morphology heat island retention. Heatwave thresholds are pegged to IMD standards (Day Maximum &ge; 40°C in plains).
      </div>
    </div>
  );
}
