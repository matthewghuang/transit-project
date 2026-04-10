import React from 'react';
import { TimeTriad } from './TimeTriad';
import { Carousel } from './Carousel';
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
        
        {!loading && !error && arrivals && arrivals.length > 0 && (
          <section className="triad-section">
            <h3>Upcoming Buses</h3>
            <Carousel>
              {arrivals.map((arrival, index) => (
                <TimeTriad key={index} stopId={stopId} arrival={arrival} />
              ))}
            </Carousel>
          </section>
        )}
        
        {!loading && !error && (!arrivals || arrivals.length === 0) && (
           <div className="triad-empty">No upcoming buses found</div>
        )}
      </main>

    </div>
  );
};
