import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { RISK_COLORS } from '../services/api';
import { Layers, MapPin, Compass } from 'lucide-react';

// Controller component to automatically pan and zoom when city or selected ward changes
function MapViewController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center && center.length === 2 && !isNaN(center[0]) && !isNaN(center[1])) {
      map.flyTo(center, zoom, { duration: 1.2 });
    }
  }, [center, zoom, map]);
  return null;
}

export default function MapView({
  geoData,
  selectedLocationId,
  onSelectLocation,
  currentCity,
  thermalMetric = 'heat_index'
}) {
  const [activeLayerMode, setActiveLayerMode] = useState('risk'); // 'risk' | 'thermal' | 'vulnerability'

  // Determine map center based on city
  const cityCenters = {
    'Mumbai': [19.09, 72.88],
    'Delhi NCR': [28.64, 77.25],
    'Ahmedabad': [23.02, 72.61]
  };

  const currentCenter = cityCenters[currentCity] || [19.09, 72.88];
  const zoomLevel = currentCity === 'Delhi NCR' ? 11.2 : 11.4;

  // Color generator based on active map layer mode
  const getFeatureColor = (props) => {
    if (activeLayerMode === 'vulnerability') {
      const v = props.vulnerability_score || 50;
      if (v < 35) return '#10b981';
      if (v < 55) return '#f59e0b';
      if (v < 70) return '#f97316';
      if (v < 85) return '#ef4444';
      return '#991b1b';
    }

    if (activeLayerMode === 'thermal') {
      const t = props.heat_index_c || props.temperature_c || 35;
      if (t < 30) return '#10b981';
      if (t < 36) return '#f59e0b';
      if (t < 42) return '#f97316';
      if (t < 50) return '#ef4444';
      return '#991b1b';
    }

    // Default: 'risk' category
    const cat = props.risk_category || 'MODERATE';
    return RISK_COLORS[cat] || '#64748b';
  };

  // GeoJSON style callback
  const styleFeature = (feature) => {
    const props = feature.properties || {};
    const isSelected = props.id === selectedLocationId;
    const color = getFeatureColor(props);

    return {
      fillColor: color,
      fillOpacity: isSelected ? 0.75 : 0.45,
      color: isSelected ? '#fbbf24' : color, // Highlight border in gold if selected
      weight: isSelected ? 3.5 : 1.5,
      dashArray: isSelected ? '4 2' : null,
      transition: 'all 0.25s ease'
    };
  };

  // Event handlers for polygons
  const onEachFeature = (feature, layer) => {
    const props = feature.properties || {};

    layer.on({
      click: () => {
        if (onSelectLocation && props.id) {
          onSelectLocation(props.id);
        }
      },
      mouseover: (e) => {
        const l = e.target;
        l.setStyle({
          weight: 3.5,
          fillOpacity: 0.8
        });
      },
      mouseout: (e) => {
        const l = e.target;
        const isSelected = props.id === selectedLocationId;
        l.setStyle({
          weight: isSelected ? 3.5 : 1.5,
          fillOpacity: isSelected ? 0.75 : 0.45
        });
      }
    });

    const popupHtml = `
      <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #0f172a; min-width: 170px;">
        <div style="font-weight: 700; font-size: 13px; margin-bottom: 2px;">${props.name}</div>
        <div style="color: #64748b; font-size: 11px; margin-bottom: 8px;">${props.district} · ${props.city}</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
          <span style="color: #475569;">Air Temp:</span>
          <b>${props.temperature_c}°C</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
          <span style="color: #475569;">Heat Index:</span>
          <b>${props.heat_index_c}°C</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
          <span style="color: #475569;">WBGT Outdoor:</span>
          <b>${props.wbgt_outdoor_c}°C</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="color: #475569;">Vulnerability:</span>
          <b>${props.vulnerability_score}/100</b>
        </div>
        <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: 600; font-size: 11px;">Risk Category:</span>
          <span style="background-color: ${RISK_COLORS[props.risk_category] || '#64748b'}; color: #fff; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px;">
            ${props.risk_category}
          </span>
        </div>
      </div>
    `;
    layer.bindPopup(popupHtml);
  };

  return (
    <div className="gis-map-panel">
      {/* Map Control Bar */}
      <div className="map-toolbar">
        <div className="map-title-row">
          <MapPin className="w-4 h-4 text-orange-400 mr-1.5" />
          <span className="map-title">Localized Ward & Grid Risk Map</span>
          <span className="map-city-badge">{currentCity}</span>
        </div>

        <div className="map-layer-selector">
          <span className="layer-label">Layer:</span>
          <button
            type="button"
            className={`layer-btn ${activeLayerMode === 'risk' ? 'active' : ''}`}
            onClick={() => setActiveLayerMode('risk')}
          >
            AI Heat Risk
          </button>
          <button
            type="button"
            className={`layer-btn ${activeLayerMode === 'thermal' ? 'active' : ''}`}
            onClick={() => setActiveLayerMode('thermal')}
          >
            Thermal Stress
          </button>
          <button
            type="button"
            className={`layer-btn ${activeLayerMode === 'vulnerability' ? 'active' : ''}`}
            onClick={() => setActiveLayerMode('vulnerability')}
          >
            Vulnerability
          </button>
        </div>
      </div>

      {/* Interactive Leaflet Map Container */}
      <div className="map-canvas-container">
        <MapContainer
          center={currentCenter}
          zoom={zoomLevel}
          className="leaflet-map-element"
          zoomControl={true}
          scrollWheelZoom={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapViewController center={currentCenter} zoom={zoomLevel} />

          {geoData && (
            <GeoJSON
              key={`${currentCity}-${selectedLocationId}-${activeLayerMode}-${JSON.stringify(geoData).length}`}
              data={geoData}
              style={styleFeature}
              onEachFeature={onEachFeature}
            />
          )}
        </MapContainer>

        {/* Floating Interactive Legend */}
        <div className="map-floating-legend">
          <div className="legend-title">
            {activeLayerMode === 'risk' && 'Heatwave Risk Level'}
            {activeLayerMode === 'thermal' && 'Thermal Stress Index (°C)'}
            {activeLayerMode === 'vulnerability' && 'Vulnerability Score'}
          </div>
          <div className="legend-items">
            {activeLayerMode === 'risk' &&
              Object.entries(RISK_COLORS).map(([cat, color]) => (
                <div key={cat} className="legend-item">
                  <span className="legend-swatch" style={{ backgroundColor: color }}></span>
                  <span className="legend-text">{cat}</span>
                </div>
              ))}

            {activeLayerMode === 'thermal' && (
              <>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#10b981' }}></span><span className="legend-text">&lt; 30°C (Low)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#f59e0b' }}></span><span className="legend-text">30–36°C (Moderate)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#f97316' }}></span><span className="legend-text">36–42°C (High)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#ef4444' }}></span><span className="legend-text">42–50°C (Very High)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#991b1b' }}></span><span className="legend-text">&gt; 50°C (Extreme)</span></div>
              </>
            )}

            {activeLayerMode === 'vulnerability' && (
              <>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#10b981' }}></span><span className="legend-text">&lt; 35 (Low)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#f59e0b' }}></span><span className="legend-text">35–55 (Moderate)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#f97316' }}></span><span className="legend-text">55–70 (High)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#ef4444' }}></span><span className="legend-text">70–85 (Very High)</span></div>
                <div className="legend-item"><span className="legend-swatch" style={{ backgroundColor: '#991b1b' }}></span><span className="legend-text">&gt; 85 (Critical)</span></div>
              </>
            )}
          </div>
          <div className="legend-hint">Click any ward to inspect localized risk</div>
        </div>
      </div>
    </div>
  );
}
