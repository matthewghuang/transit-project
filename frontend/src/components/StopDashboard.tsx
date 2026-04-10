import React from 'react';
import { TimeTriad } from './TimeTriad';

interface StopDashboardProps {
  stopId: string;
  onBack: () => void;
}

export const StopDashboard: React.FC<StopDashboardProps> = ({ stopId, onBack }) => {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <button className="back-btn" onClick={onBack}>
          ← Search
        </button>
        <div className="stop-title">
          <h2>Stop #{stopId}</h2>
        </div>
      </header>

      <main className="dashboard-main">
        <section className="triad-section">
          <h3>Next Arrival</h3>
          <TimeTriad stopId={stopId} />
        </section>

        <section className="info-section">
          <div className="info-card">
            <h4>About this stop</h4>
            <p>Reliability data is based on historical observations for this specific time of day.</p>
          </div>
        </section>
      </main>
    </div>
  );
};
