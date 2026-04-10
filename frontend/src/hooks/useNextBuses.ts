import { useQuery } from "@tanstack/react-query";
import ky from "ky";

export interface NextBusesResponse {
  stop_id: string;
  route_id: string | null;
  route_name: string | null;
  scheduled_time: string | null;
  actual_time: string | null;
  predicted_time: string | null;
  arrive_by_time: string | null;
  confidence: number;
  low_confidence: boolean;
  is_stale: boolean;
  last_updated: string | null;
}

export function useNextBuses(stopId: string | null, confidence: number = 95) {
  const { data, isLoading, error } = useQuery<NextBusesResponse[]>({
    queryKey: ["next_buses", stopId, confidence],
    queryFn: () =>
      ky
        .get(`/api/stops/${stopId}/next_buses`, {
          searchParams: { confidence },
        })
        .json(),
    enabled: !!stopId,
    refetchInterval: 30000, // Refresh every 30s for staleness detection
  });

  return { data, loading: isLoading, error };
}
