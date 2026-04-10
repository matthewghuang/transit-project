import React from 'react';
import { TimeTriad } from './TimeTriad';
import { useStops } from '../hooks/useStops';

interface StopDashboardProps {
  stopId: string;
  onBack: () => void;
}

export const StopDashboard: React.FC<StopDashboardProps> = ({ stopId, onBack }) => {
  const { data: stops } = useStops();
  const stop = stops?.find(s => s.id === stopId);
  const stopName = stop ? stop.name : `Stop #${stopId}`;

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <button className="back-btn" onClick={onBack}>
          ← Search
        </button>
        <div className="stop-title">
          <h2>{stopName} {stop && <span className="stop-id-sub">(#{stopId})</span>}</h2>
        </div>
      </header>

      <main className="dashboard-main">
        <section className="triad-section">
          <h3>Next Arrival</h3>
          <TimeTriad stopId={stopId} />
        </section>
      </main>

    </div>
  );
};
