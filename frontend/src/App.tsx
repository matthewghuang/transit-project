import "./App.css";
import { Map } from "./components/Map";
import { FilterTable } from "./components/FilterTable";
import { usePositions } from "./hooks/usePositions";

export function App() {
  const { data, isLoading } = usePositions();

  if (isLoading) {
    return (
      <>
        <p>Loading!</p>
      </>
    );
  } else {
    return (
      <>
        <header>
          <h1>Real-Time Transit Dashboard</h1>
        </header>
        <main>
          <div className="map">
            <Map style={{ height: "100%" }}></Map>
          </div>
          <div className="filter">
            <FilterTable></FilterTable>
          </div>
        </main>
      </>
    );
  }
}
