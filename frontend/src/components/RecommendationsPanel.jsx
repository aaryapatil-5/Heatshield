import React, { useState } from 'react';
import { ClipboardList, Users, HardHat, Building, Stethoscope, CheckCircle } from 'lucide-react';

export default function RecommendationsPanel({ recommendationsList }) {
  const [activeRoleIndex, setActiveRoleIndex] = useState(0);

  if (!recommendationsList || recommendationsList.length === 0) {
    return <div className="panel empty-state">No specific operational recommendations generated.</div>;
  }

  const roleIcons = [Users, HardHat, Building, Stethoscope];

  return (
    <div className="panel recommendations-panel">
      <div className="panel-header-row">
        <div>
          <div className="panel-title-wrap">
            <ClipboardList className="w-5 h-5 text-orange-400 mr-2" />
            <h2 className="panel-title">Heat Action Plan (HAP) Targeted Interventions</h2>
          </div>
          <p className="panel-subtitle">
            Role-calibrated disaster risk reduction measures aligned with National Disaster Management Authority (NDMA) guidelines
          </p>
        </div>
      </div>

      {/* Role Navigation Tabs */}
      <div className="role-tabs-bar">
        {recommendationsList.map((rec, idx) => {
          const Icon = roleIcons[idx % roleIcons.length];
          const isActive = idx === activeRoleIndex;

          return (
            <button
              key={rec.audience || idx}
              type="button"
              className={`role-tab-btn ${isActive ? 'active' : ''}`}
              onClick={() => setActiveRoleIndex(idx)}
            >
              <Icon className="w-4 h-4 mr-2" />
              <span>{rec.audience}</span>
              {rec.priority === 'Urgent' && <span className="urgent-dot"></span>}
            </button>
          );
        })}
      </div>

      {/* Active Role Content Card */}
      {recommendationsList[activeRoleIndex] && (
        <div className="role-content-box">
          <div className="role-content-header">
            <div>
              <h3 className="role-content-title">
                {recommendationsList[activeRoleIndex].audience} Protocols
              </h3>
              <span className="role-badge-tag">
                {recommendationsList[activeRoleIndex].badge || 'Disaster Mitigation'}
              </span>
            </div>
            <span
              className={`priority-pill ${
                recommendationsList[activeRoleIndex].priority === 'Urgent' ? 'urgent' : 'normal'
              }`}
            >
              Priority: {recommendationsList[activeRoleIndex].priority}
            </span>
          </div>

          <div className="action-items-list">
            {recommendationsList[activeRoleIndex].actions.map((act, aIdx) => (
              <div key={aIdx} className="action-item-card">
                <div className="action-number-badge">{aIdx + 1}</div>
                <div className="action-item-text">{act}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
