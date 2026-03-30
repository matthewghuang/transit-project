import "./App.css";
import { Map } from "./components/Map";
import { FilterTable } from "./components/FilterTable";
import { usePositions } from "./hooks/usePositions";

export function App() {
  const { isLoading } = usePositions();

  if (isLoading) {
    return (
      <div className="loading-container">
        <p>Initializing Real-Time Data...</p>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header>
        <h1>Transit Dashboard</h1>
      </header>
      <main>
        <div className="map-container">
          <Map style={{ height: "100%" }} />
        </div>
        <aside className="sidebar">
          <FilterTable />
        </aside>
      </main>
    </div>
  );
}
