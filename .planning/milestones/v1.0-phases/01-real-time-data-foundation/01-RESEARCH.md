---
phase: 01
name: Real-time Data Foundation
goal: Establish a high-performance join between static schedules and real-time feeds to derive discrete delay metrics.
date: 2026-04-09
---

# Phase 1 Research: Real-time Data Foundation

## Domain Analysis

The core challenge of this phase is calculating real-time lateness by joining GTFS-Realtime `TripUpdate` messages with static GTFS `stop_times.txt`. 

### Key Concepts
- **GTFS-Static**: Defines the ground truth schedules. `stop_times.txt` contains `trip_id`, `stop_id`, and `arrival_time`.
- **GTFS-Realtime (TripUpdates)**: Provides `StopTimeUpdate` events. These specify `stop_id` and either `arrival` or `departure` with a `delay` field (in seconds).
- **Temporal Anchor**: Lateness is relative to the `header.timestamp` of the feed to ensure consistency.

## Technical Approach

### 1. High-Performance Join (D-01, D-02)
To achieve O(1) lookups during stream processing, we will load `stop_times.txt` into an in-memory dictionary.
- **Data Structure**: `{(trip_id, stop_id): scheduled_arrival_seconds}`.
- **Parsing**: Use `pandas` for efficient loading of the 90MB file.
- **Conversion**: All `arrival_time` strings (e.g., "06:16:00") will be converted to "seconds from midnight" to allow direct comparison with UNIX timestamps (modulo 86400).

### 2. Delay Calculation Logic (D-03, D-04)
The new `delay_consumer.py` will:
1. Listen to a `trip_update` Kafka topic.
2. For each `StopTimeUpdate` in a `TripUpdate`:
   - Identify the `stop_id`.
   - Retrieve the `scheduled_arrival_time` from the in-memory cache.
   - Calculate `lateness = actual_arrival_time - scheduled_arrival_time`.
   - Per **D-03**, explicitly use the `delay` field provided in the protobuf if available, or calculate it if `time` is provided.

### 3. Kafka Topology
`main.py` currently polls a generic `position_url`. It needs to be updated or augmented to poll the `realtime_url` (GTFS-R TripUpdates) and publish to a new topic `trip_updates`.

### 4. Frontend Integration (D-05, D-06)
- **State**: The `usePositions` hook will be updated or a new `useDelays` hook created to fetch enriched vehicle data including delay info.
- **UI**: Leaflet `Popup` components will be used to show "X minutes late" when a user clicks a vehicle marker or stop.

## Validation Architecture

### Automated Verification
- **Unit Tests**: Test the static schedule loader with edge cases (e.g., trips crossing midnight).
- **Integration Tests**: Verify that a sample `TripUpdate` message results in the correct MongoDB document with `delay_seconds` field.
- **Load Test**: Ensure the consumer handles the Translink poll rate (30s) without falling behind Kafka offsets.

### Manual Verification
- Clicking a vehicle on the map and verifying the popup shows "Minutes Away" or "Lateness" matching the raw GTFS-R feed.

## Pitfalls & Mitigations
- **Midnight Crossover**: GTFS times can exceed 24:00:00. The parser must handle "25:30:00" correctly.
- **Memory Usage**: Storing 90MB of stop times in memory is acceptable (~1-2M rows), but we should monitor RSS.
- **Missing Data**: Some vehicles might not have `TripUpdates`. UI must handle "No real-time data" gracefully.
