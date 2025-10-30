import ky from "ky";

export type VehiclePosition = {
  latitude: number;
  longitude: number;
};

export type VehicleInfo = {
  id: string;
  label: string;
};

export type VehicleTrip = {
  routeId: string;
  directionId: number;
  route_name: string;
  scheduleRelationship: string;
  startDate: string;
  tripId: string;
};

export type Vehicle = {
  position: VehiclePosition;
  currentStopSequence: number;
  currentStatus: string;
  timestamp: string;
  stopId: string;
  vehicle: VehicleInfo;
  trip: VehicleTrip;
};

export type PositionDocumentEntry = {
  id: string;
  vehicle: Vehicle;
  timestamp: string;
  _id: string;
};

export const fetchPositions = async (): Promise<PositionDocumentEntry[]> => {
  const response = await ky.get("api/vehicles");

  if (!response.ok) throw new Error(`Request error: ${response.status}`);

  return response.json();
};
