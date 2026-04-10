import React from 'react';
import { TimeTriad } from './TimeTriad';
import { useStops } from '../hooks/useStops';
import { useNextBuses } from '../hooks/useNextBuses';
import { useFilterStore } from '../stores/filterStore';

interface StopDashboardProps {
  stopId: string;
  onBack: () => void;
}

export const StopDashboard: React.FC<StopDashboardProps> = ({ stopId, onBack }) => {
  const { data: stops } = useStops();
  const confidenceLevel = useFilterStore((state) => state.confidenceLevel);
  const { data: arrivals, loading, error } = useNextBuses(stopId, confidenceLevel);

  const stop = stops?.find(s => s.id === stopId);
  const stopName = stop ? stop.name : `Stop #${stopId}`;

  const firstArrival = (arrivals && arrivals.length > 0) ? arrivals[0] : null;

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
        {loading && <div className="triad-loading">Loading predictions...</div>}
        {error && <div className="triad-error">Failed to load predictions</div>}
        
        {!loading && !error && firstArrival && (
          <section className="triad-section">
            <h3>Next Arrival</h3>
            <TimeTriad stopId={stopId} arrival={firstArrival} />
          </section>
        )}
        
        {!loading && !error && !firstArrival && (
           <div className="triad-empty">No upcoming buses found</div>
        )}
      </main>

    </div>
  );
};
