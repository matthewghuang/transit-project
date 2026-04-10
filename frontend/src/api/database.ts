import ky from "ky";

export type VehiclePosition = {
  latitude: number;
  longitude: number;
};

export type VehicleTrip = {
  tripId: string;
  routeId: string;
  routeName: string;
};

// Matches the flat VehicleUpdate shape returned by the TimescaleDB API
export type VehicleUpdate = {
  id: string;
  trip: VehicleTrip;
  position: VehiclePosition;
  timestamp: string;
};

export type StopInfo = {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  observation_count: number;
};

export const fetchPositions = async (): Promise<VehicleUpdate[]> => {
  const response = await ky.get("api/vehicles");

  if (!response.ok) throw new Error(`Request error: ${response.status}`);

  return response.json();
};

export const fetchStops = async (): Promise<StopInfo[]> => {
  const response = await ky.get("api/stops");

  if (!response.ok) throw new Error(`Request error: ${response.status}`);

  return response.json();
};
