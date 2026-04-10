import React from "react";
import { useQuery } from "@tanstack/react-query";
import ky from "ky";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

interface Bucket {
  minute: number;
  count: number;
}

interface DistributionData {
  stop_id: string;
  median: number;
  p05: number | null;
  p95: number | null;
  observation_count: number;
  buckets: Bucket[];
}

const DelayDistributionChart: React.FC<{ stopId: string }> = ({ stopId }) => {
  const { data, isLoading, error } = useQuery<DistributionData>({
    queryKey: ["distribution", stopId],
    queryFn: () => ky.get(`/api/distribution/${stopId}`).json(),
  });

  if (isLoading) return <div style={{ padding: "10px", textAlign: "center" }}>Loading distribution...</div>;
  if (error) return <div style={{ padding: "10px", color: "red" }}>Error loading distribution</div>;
  if (!data || data.buckets.length === 0) {
    return <div style={{ padding: "10px", fontStyle: "italic" }}>No distribution data available for this stop</div>;
  }

  // Sort buckets by minute for correct charting
  const sortedBuckets = [...data.buckets].sort((a, b) => a.minute - b.minute);

  return (
    <div style={{ marginTop: "12px", borderTop: "1px solid #eee", paddingTop: "12px" }}>
      <div style={{ marginBottom: "8px", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "4px" }}>
        <strong>Delay Distribution</strong>
        <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
          <span style={{ 
            background: "#e8f5e9", 
            color: "#2e7d32", 
            padding: "2px 6px", 
            borderRadius: "4px",
            fontSize: "0.85em",
            fontWeight: "bold"
          }}>
            Median: {data.median.toFixed(1)}m
          </span>
          {data.p95 !== null && (
            <span style={{ 
              background: "#fff3e0", 
              color: "#e65100", 
              padding: "2px 6px", 
              borderRadius: "4px",
              fontSize: "0.85em",
              fontWeight: "bold"
            }}>
              P95: {data.p95.toFixed(1)}m
            </span>
          )}
        </div>
      </div>
      
      <div style={{ width: "100%", height: 120 }}>
        <ResponsiveContainer>
          <AreaChart data={sortedBuckets} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis 
              dataKey="minute" 
              fontSize={10} 
              tickFormatter={(tick) => `${tick}m`}
            />
            <YAxis hide />
            <Tooltip 
              labelFormatter={(label) => `${label} minutes delay`}
              formatter={(value: number) => [value, "Observations"]}
              contentStyle={{ fontSize: "12px" }}
            />
            {/* ADV-01: P95 reference line */}
            {data.p95 !== null && (
              <ReferenceLine
                x={Math.round(data.p95)}
                stroke="#e65100"
                strokeDasharray="4 2"
                label={{ value: "95%", position: "top", fontSize: 9, fill: "#e65100" }}
              />
            )}
            {/* Median reference line */}
            <ReferenceLine
              x={Math.round(data.median)}
              stroke="#2e7d32"
              strokeDasharray="4 2"
              label={{ value: "Med", position: "top", fontSize: 9, fill: "#2e7d32" }}
            />
            <Area
              type="monotone"
              dataKey="count"
              stroke="#2e7d32"
              fill="#81c784"
              fillOpacity={0.6}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div style={{ fontSize: "0.75em", color: "#999", textAlign: "center", marginTop: "4px" }}>
        Minutes relative to schedule ({data.observation_count} observations)
      </div>
    </div>
  );
};

export default DelayDistributionChart;
