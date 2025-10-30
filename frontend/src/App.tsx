import "./App.css";
import { Map } from "./Map";
import { usePositions } from "./hooks/usePositions";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export function App() {
  return (
    <>
      <QueryClientProvider client={queryClient}>
        <Map className="map"></Map>
      </QueryClientProvider>
    </>
  );
}
