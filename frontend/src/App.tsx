import { useState } from "react";
import "./App.css";
import { HeroSearch } from "./components/HeroSearch";

export function App() {
  const [selectedStopId, setSelectedStopId] = useState<string | null>(null);

  return (
    <div className="app-container">
      <header>
        <h1 onClick={() => setSelectedStopId(null)} style={{ cursor: 'pointer' }}>
          Transit Dashboard
        </h1>
      </header>
      <main>
        {!selectedStopId ? (
          <HeroSearch onSelectStop={setSelectedStopId} />
        ) : (
          <div className="dashboard-container">
            <button className="btn" onClick={() => setSelectedStopId(null)} style={{ margin: '1rem' }}>
              ← Back to Search
            </button>
            <div style={{ padding: '0 1rem' }}>
              <h2>Stop Dashboard for {selectedStopId}</h2>
              <p>Dashboard components coming in next plan...</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
