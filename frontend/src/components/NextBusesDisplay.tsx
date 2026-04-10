import React from 'react';
import { useNextBuses } from '../hooks/useNextBuses';

interface Props {
  stopId: string;
}

const NextBusesDisplay: React.FC<Props> = ({ stopId }) => {
  const { data, loading, error } = useNextBuses(stopId);

  if (loading) {
    return <div style={{ marginTop: '10px', fontStyle: 'italic' }}>Loading next buses...</div>;
  }

  if (error) {
    return <div style={{ marginTop: '10px', color: 'red' }}>Error loading next buses</div>;
  }

  if (!data) {
    return null;
  }

  if (!data.scheduled_time) {
    return (
      <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
        <strong>Next Bus:</strong> No upcoming buses scheduled.
      </div>
    );
  }

  return (
    <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#f0f7ff', borderRadius: '4px', border: '1px solid #cce4ff' }}>
      <strong style={{ display: 'block', marginBottom: '4px', color: '#0056b3' }}>Next Bus Predictions</strong>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px', fontSize: '0.95em' }}>
        <div><strong>Scheduled:</strong></div>
        <div>{data.scheduled_time}</div>
        
        <div><strong>Actual (Delay):</strong></div>
        <div>{data.actual_time || data.scheduled_time}</div>
        
        <div><strong>Predicted:</strong></div>
        <div style={{ fontWeight: 'bold', color: data.predicted_time && data.predicted_time > data.scheduled_time ? '#d32f2f' : '#2e7d32' }}>
          {data.predicted_time || data.scheduled_time}
        </div>
      </div>
    </div>
  );
};

export default NextBusesDisplay;
