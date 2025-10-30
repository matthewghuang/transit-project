import { useQuery } from "@tanstack/react-query";
import { fetchPositions } from "../api/database";

export const usePositions = () => {
  return useQuery({
    queryKey: ["todos"],
    queryFn: fetchPositions,
    refetchInterval: 15 * 1000,
  });
};
