import React, { useState } from 'react';
import { useNextBuses } from '../hooks/useNextBuses';
import DelayDistributionChart from './DelayDistributionChart';

interface TimeTriadProps {
  stopId: string;
}

export const TimeTriad: React.FC<TimeTriadProps> = ({ stopId }) => {
  const { data, loading, error } = useNextBuses(stopId);
  const [isExpanded, setIsExpanded] = useState(false);

  if (loading) return <div className="triad-loading">Loading predictions...</div>;
  if (error) return <div className="triad-error">Failed to load predictions</div>;
  if (!data || !data.scheduled_time) return <div className="triad-empty">No upcoming buses found</div>;

  const times = [
    { label: 'Scheduled', time: data.scheduled_time },
    { label: 'Actual', time: data.actual_time || null },
    { label: 'Predicted', time: data.predicted_time || null },
  ];

  // Hero Time logic: Priority is Actual > Predicted > Scheduled
  let heroTimeObj = { label: 'Scheduled', time: data.scheduled_time };
  let heroStatus = 'Scheduled';

  if (data.actual_time) {
    heroTimeObj = { label: 'Actual', time: data.actual_time };
    heroStatus = 'Real-time';
  } else if (data.predicted_time) {
    heroTimeObj = { label: 'Predicted', time: data.predicted_time };
    heroStatus = ''; // Prediction subtitle removed
  }

  return (
    <div className={`time-triad ${isExpanded ? 'expanded' : ''}`} onClick={() => setIsExpanded(!isExpanded)}>
      <div className="hero-time-section">
        <div className="hero-label">{heroTimeObj.label} Time</div>
        <div className="hero-display">{heroTimeObj.time}</div>
        {heroStatus && (
          <div className="hero-status">
            {heroStatus}
          </div>
        )}
      </div>

      {isExpanded && (
        <div className="triad-details">
          <div className="triad-grid">
            {times.map((t) => (
              <div key={t.label} className="triad-col">
                <div className="col-label">{t.label}</div>
                <div className="col-time">{t.time || '--:--:--'}</div>
              </div>
            ))}
          </div>
          
          <div style={{ minHeight: '180px' }}>
            <DelayDistributionChart stopId={stopId} />
          </div>
          
          <div className="triad-hint">Click to collapse</div>
        </div>
      )}
      
      {!isExpanded && (
        <div className="expand-hint">Click for details & reliability</div>
      )}
    </div>
  );
};
