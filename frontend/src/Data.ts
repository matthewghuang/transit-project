import { create } from "zustand";

type VehiclePosition = {
  latitude: number;
  longitude: number;
};

type VehicleInfo = {
  id: string;
  label: string;
};

type Vehicle = {
  tripId: string;
  startDate: string;
  scheduleRelationship: string;
  routeId: string;
  directionId: number;
  route_name: string;
  position: VehiclePosition;
  currentStopSequence: number;
  currentStatus: string;
  timestamp: string;
  stopId: string;
  vehicle: VehicleInfo;
};

type PositionDocumentEntry = {
  id: string;
  vehicle: Vehicle;
  timestamp: Date;
  _id: string;
};

interface PositionState {
  positions: PositionDocumentEntry[];
  updateData: (newData: PositionState) => void;
}

const usePosition = create<PositionState>()((set) => ({
  positions: [],
  updateData: (newData: PositionState) => set(newData),
}));

export { usePosition };
