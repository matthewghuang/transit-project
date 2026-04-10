import { useState, useEffect } from "react";

interface NextBusesResponse {
  stop_id: string;
  scheduled_time: string | null;
  actual_time: string | null;
  predicted_time: string | null;
}

export function useNextBuses(stopId: string | null) {
  const [data, setData] = useState<NextBusesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!stopId) {
      setData(null);
      return;
    }

    let isMounted = true;
    setLoading(true);

    fetch(`/api/stops/${stopId}/next_buses`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch next buses");
        return res.json();
      })
      .then((json) => {
        if (isMounted) {
          setData(json);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [stopId]);

  return { data, loading, error };
}
