import React from "react";
import { useQuery } from "@tanstack/react-query";
import ky from "ky";
import { useFilterStore } from "../stores/filterStore";
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
  const confidenceLevel = useFilterStore((state) => state.confidenceLevel);
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

  // Calculate cutoff minute for current confidence level
  const totalObservations = sortedBuckets.reduce((sum, b) => sum + b.count, 0);
  const targetCount = (confidenceLevel / 100) * totalObservations;
  
  let cumulativeCount = 0;
  let cutoffMinute = sortedBuckets[0].minute;
  for (const bucket of sortedBuckets) {
    cumulativeCount += bucket.count;
    cutoffMinute = bucket.minute;
    if (cumulativeCount >= targetCount) {
      break;
    }
  }

  // Prepare data for Recharts with shaded area
  const chartData = sortedBuckets.map(b => ({
    ...b,
    shadedCount: b.minute <= cutoffMinute ? b.count : null
  }));

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
          <span style={{ 
            background: "#fff3e0", 
            color: "#e65100", 
            padding: "2px 6px", 
            borderRadius: "4px",
            fontSize: "0.85em",
            fontWeight: "bold"
          }}>
            {confidenceLevel}%: {cutoffMinute}m
          </span>
        </div>
      </div>
      
      <div style={{ width: "100%", height: 120 }}>
        <ResponsiveContainer>
          <AreaChart data={chartData} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
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
            
            <ReferenceLine
              x={cutoffMinute}
              stroke="#2563eb"
              strokeDasharray="4 2"
              label={{ value: `${confidenceLevel}%`, position: "top", fontSize: 9, fill: "#2563eb" }}
            />

            <ReferenceLine
              x={Math.round(data.median)}
              stroke="#2e7d32"
              strokeDasharray="4 2"
              label={{ value: "Med", position: "top", fontSize: 9, fill: "#2e7d32" }}
            />
            
            {/* Base Area */}
            <Area
              type="monotone"
              dataKey="count"
              stroke="#2e7d32"
              fill="#81c784"
              fillOpacity={0.2}
              isAnimationActive={false}
            />
            
            {/* Confidence Area */}
            <Area
              type="monotone"
              dataKey="shadedCount"
              stroke="#2563eb"
              fill="#2563eb"
              fillOpacity={0.2}
              isAnimationActive={false}
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
