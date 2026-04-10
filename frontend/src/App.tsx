import { useState } from "react";
import "./App.css";
import { HeroSearch } from "./components/HeroSearch";
import { StopDashboard } from "./components/StopDashboard";

export function App() {
  const [selectedStopId, setSelectedStopId] = useState<string | null>(null);

  return (
    <div className="app-container">
      {!selectedStopId ? (
        <main>
          <HeroSearch onSelectStop={setSelectedStopId} />
        </main>
      ) : (
        <StopDashboard 
          stopId={selectedStopId} 
          onBack={() => setSelectedStopId(null)} 
        />
      )}
    </div>
  );
}
