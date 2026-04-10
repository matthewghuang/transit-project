import { useQuery } from "@tanstack/react-query";
import { fetchStops } from "../api/database";

export const useStops = () => {
  return useQuery({
    queryKey: ["stops"],
    queryFn: fetchStops,
    refetchInterval: 60 * 1000,
    staleTime: 30 * 1000,
  });
};
