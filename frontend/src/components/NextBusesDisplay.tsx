import React from 'react';
import { useNextBuses } from '../hooks/useNextBuses';

interface Props {
  stopId: string;
}

const NextBusesDisplay: React.FC<Props> = ({ stopId }) => {
  const { data, loading, error } = useNextBuses(stopId);

  return (
    <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#f0f7ff', borderRadius: '4px', border: '1px solid #cce4ff' }}>
      <div style={{ display: 'none' }}>
        DEBUG: {JSON.stringify({ stopId, loading, error: error?.message, data })}
      </div>
      <strong style={{ display: 'block', marginBottom: '4px', color: '#0056b3' }}>Next Bus Predictions</strong>
      
      {loading && <div>Loading next buses...</div>}
      {error && <div style={{ color: 'red' }}>Error: {error.message}</div>}
      
      {!loading && !error && !data && <div>No data received.</div>}
      
      {!loading && !error && data && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px', fontSize: '0.95em' }}>
          <div><strong>Scheduled:</strong></div>
          <div>{data.scheduled_time || 'None'}</div>
          
          <div><strong>Actual (Delay):</strong></div>
          <div>{data.actual_time || data.scheduled_time || 'None'}</div>
          
          <div><strong>Predicted:</strong></div>
          <div style={{ fontWeight: 'bold' }}>
            {data.predicted_time || data.scheduled_time || 'None'}
          </div>
        </div>
      )}
    </div>
  );
};

export default NextBusesDisplay;
