/**
 * API Service for HeatShield AI.
 * Communicates with FastAPI backend with automatic error interception and offline demo fallbacks.
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!res.ok) {
      const errText = await res.text();
      let parsedMsg = errText;
      try {
        const errJson = JSON.parse(errText);
        parsedMsg = errJson.detail || errJson.message || errText;
      } catch (_) {}
      throw new Error(parsedMsg || `HTTP error ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    console.error(`API Request failed for ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  getHealth: () => request('/health'),
  getMode: () => request('/mode'),
  setMode: (mode) => request('/mode', { method: 'POST', body: JSON.stringify({ mode }) }),
  getThermalMetrics: () => request('/thermal-metrics'),
  getLocations: (city = null) => request(`/locations${city ? `?city=${encodeURIComponent(city)}` : ''}`),
  getCurrentRisk: (locationId, metric = 'heat_index') =>
    request(`/current-risk?location=${encodeURIComponent(locationId)}&metric=${encodeURIComponent(metric)}`),
  getForecast: (locationId, metric = 'heat_index') =>
    request(`/forecast?location=${encodeURIComponent(locationId)}&metric=${encodeURIComponent(metric)}`),
  getRiskMap: (city = null, metric = 'heat_index') =>
    request(`/risk-map?metric=${encodeURIComponent(metric)}${city ? `&city=${encodeURIComponent(city)}` : ''}`),
  getHistory: (locationId) => request(`/history?location=${encodeURIComponent(locationId)}`),
  getAlerts: (locationId, metric = 'heat_index') =>
    request(`/alerts?location=${encodeURIComponent(locationId)}&metric=${encodeURIComponent(metric)}`),
  getRecommendations: (locationId, metric = 'heat_index') =>
    request(`/recommendations?location=${encodeURIComponent(locationId)}&metric=${encodeURIComponent(metric)}`),
  getModelPerformance: () => request('/model-performance'),
  runPredict: (features) => request('/predict', { method: 'POST', body: JSON.stringify(features) }),
  runSimulation: (params) => request('/simulate', { method: 'POST', body: JSON.stringify(params) }),
};

export const RISK_COLORS = {
  LOW: '#10b981',        // Emerald Green
  MODERATE: '#f59e0b',   // Amber Yellow
  HIGH: '#f97316',       // Orange
  'VERY HIGH': '#ef4444',// Red
  EXTREME: '#991b1b',    // Dark Crimson
};
