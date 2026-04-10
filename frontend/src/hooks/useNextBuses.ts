import { useQuery } from "@tanstack/react-query";
import ky from "ky";

interface NextBusesResponse {
  stop_id: string;
  scheduled_time: string | null;
  actual_time: string | null;
  predicted_time: string | null;
  arrive_by_time: string | null;
  is_stale: boolean;
  last_updated: string | null;
}

export function useNextBuses(stopId: string | null) {
  const { data, isLoading, error } = useQuery<NextBusesResponse>({
    queryKey: ["next_buses", stopId],
    queryFn: () => ky.get(`/api/stops/${stopId}/next_buses`).json(),
    enabled: !!stopId,
    refetchInterval: 30000, // Refresh every 30s for staleness detection
  });

  return { data, loading: isLoading, error };
}
