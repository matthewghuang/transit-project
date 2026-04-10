import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import ky from 'ky';
import { NextBusesResponse } from '../hooks/useNextBuses';
import { useFilterStore } from '../stores/filterStore';
import DelayDistributionChart from './DelayDistributionChart';

interface TimeTriadProps {
  stopId: string;
  arrival: NextBusesResponse;
}

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

export const TimeTriad: React.FC<TimeTriadProps> = ({ stopId, arrival }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const confidenceLevel = useFilterStore((state) => state.confidenceLevel);
  const setConfidenceLevel = useFilterStore((state) => state.setConfidenceLevel);

  // Fetch distribution data for zero-latency arrive-by calculation
  const { data: distData } = useQuery<DistributionData>({
    queryKey: ["distribution", stopId],
    queryFn: () => ky.get(`/api/distribution/${stopId}`).json(),
    enabled: !!stopId && isExpanded,
  });

  if (!arrival || !arrival.scheduled_time) return <div className="triad-empty">No upcoming buses found</div>;

  // Local Arrive-By Calculation (Zero-latency)
  let arriveByDisplay = arrival.arrive_by_time;
  
  if (distData && distData.buckets.length > 0 && arrival.scheduled_time) {
    const sortedBuckets = [...distData.buckets].sort((a, b) => a.minute - b.minute);
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

    // Calculate arrive by: scheduled_time (HH:MM:SS) - cutoffMinute
    const [h, m, s] = arrival.scheduled_time.split(':').map(Number);
    const scheduledDate = new Date();
    scheduledDate.setHours(h, m, s, 0);
    
    const arriveByDate = new Date(scheduledDate.getTime() - cutoffMinute * 60000);
    arriveByDisplay = arriveByDate.toTimeString().split(' ')[0];
  }

  const times = [
    { label: 'Scheduled', time: arrival.scheduled_time },
    { label: 'Actual', time: arrival.actual_time || null },
    { label: 'Predicted', time: arrival.predicted_time || null },
  ];

  // Hero Time logic: Priority is Actual > Predicted > Scheduled
  let heroTimeObj = { label: 'Scheduled', time: arrival.scheduled_time };
  let heroStatus = 'Scheduled';

  if (arrival.actual_time) {
    heroTimeObj = { label: 'Actual', time: arrival.actual_time };
    heroStatus = 'Real-time';
  } else if (arrival.predicted_time) {
    heroTimeObj = { label: 'Predicted', time: arrival.predicted_time };
    heroStatus = '';
  }

  return (
    <div className={`time-triad ${isExpanded ? 'expanded' : ''}`} onClick={(e) => {
      // Don't collapse when clicking the slider
      if ((e.target as HTMLElement).closest('.reliability-slider')) return;
      setIsExpanded(!isExpanded);
    }}>
      {/* ADV-02: Ghost bus warning banner */}
      {arrival.is_stale && (
        <div className="ghost-bus-warning">
          <span className="ghost-icon">&#x26A0;</span>
          <span>Stale Data — GPS lost{arrival.last_updated ? ` (last update: ${arrival.last_updated})` : ''}</span>
        </div>
      )}

      {arrival.route_name && (
        <div className="route-header">
          <span className="route-label">Route</span>
          <span className="route-name">{arrival.route_name}</span>
        </div>
      )}

      <div className="hero-time-section">
        <div className="hero-label">{heroTimeObj.label} Time</div>
        <div className={`hero-display ${arrival.is_stale ? 'stale' : ''}`}>{heroTimeObj.time}</div>
        {heroStatus && (
          <div className="hero-status">
            {heroStatus}
          </div>
        )}
      </div>

      {/* ADV-01: Arrive-by recommendation */}
      {(arriveByDisplay || arrival.arrive_by_time) && (
        <div className="arrive-by-section">
          <div className="arrive-by-label">Arrive by</div>
          <div className="arrive-by-time">{arriveByDisplay || arrival.arrive_by_time}</div>
          <div className="arrive-by-confidence">{confidenceLevel}% confidence</div>
        </div>
      )}

      {isExpanded && (
        <div className="triad-details">
          <div className="triad-grid">
            {times.map((t) => (
              <div key={t.label} className="triad-col">
                <div className="col-label">{t.label}</div>
                <div className="col-time">{t.time || '--:--:--'}</div>
              </div>
            ))}
          </div>

          <div className="reliability-slider" style={{ marginTop: '16px', padding: '0 8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span style={{ fontSize: '12px', fontWeight: 600 }}>Reliability Threshold</span>
              <span style={{ fontSize: '12px', color: '#2563eb', fontWeight: 700 }}>{confidenceLevel}% certainty</span>
            </div>
            <input 
              type="range" 
              min="50" 
              max="99" 
              step="1"
              value={confidenceLevel} 
              onChange={(e) => setConfidenceLevel(parseInt(e.target.value))}
              style={{ width: '100%', cursor: 'pointer' }}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#666', marginTop: '2px' }}>
              <span>50%</span>
              <span>75%</span>
              <span>90%</span>
              <span>95%</span>
              <span>99%</span>
            </div>
          </div>
          
          <div style={{ minHeight: '180px' }}>
            <DelayDistributionChart stopId={stopId} />
          </div>
          
          <div className="triad-hint">Click to collapse</div>
        </div>
      )}
      
      {!isExpanded && (
        <div className="expand-hint">Click for details & reliability</div>
      )}
    </div>
  );
};
