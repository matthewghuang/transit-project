# Domain Pitfalls

**Domain:** Transit Data Analysis (GTFS-R)
**Researched:** April 09, 2026

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: Clock Drift and Timestamp Misalignment
**What goes wrong:** Real-time delay calculations often involve subtracting a "scheduled time" from an "actual arrival time." If the server clock fetching the data differs from the agency's clock, or if `header.timestamp` is ignored in favor of local arrival time, the data becomes skewed.
**Why it happens:** Developers assume "now" is the correct reference point for real-time feeds, but GTFS-RT feeds are snapshots of a specific moment in the past (often 30-60s old).
**Consequences:** Systematic bias in delay distributions (e.g., all buses appearing 30s later than they are).
**Prevention:** Always use the `header.timestamp` from the feed as the reference point for "current" time. Synchronize processing servers via NTP.
**Detection:** Check if delay distributions have a strange "floor" or "ceiling" (e.g., no bus ever arriving less than 30s late).

### Pitfall 2: Handling Trip Cancellations as "Missing Data"
**What goes wrong:** When a trip is cancelled (`SCHEDULE_RELATIONSHIP: CANCELED`), it often disappears from the active feed. If the system only tracks "observed" delays, it misses the worst-case scenario: the bus that never came.
**Why it happens:** Most analysis logic is triggered by the presence of a `VehiclePosition` or `TripUpdate`.
**Consequences:** Reliability metrics look better than they actually are because total failures (cancellations) are ignored.
**Prevention:** Implement a "Dead Man's Switch" for trips. If a trip is in the static schedule but flagged as `CANCELED` in the feed (or missing entirely after its start time), record it as a "canceled" event rather than a null value.
**Detection:** Comparison of total trips in static schedule vs. total observations in the database.

### Pitfall 3: The "Ghost Bus" (Stale Data) Problem
**What goes wrong:** A vehicle stops sending updates but remains in the feed with an old timestamp. A naive consumer might keep reporting the last known delay.
**Why it happens:** Agencies sometimes fail to prune stale entities from their Protobuf output.
**Consequences:** Distribution curves get "stretched" by old data points, and the dashboard shows "live" buses that are actually parked in a garage.
**Prevention:** Validate the `timestamp` on individual `TripUpdate` or `VehiclePosition` entities. If the entity timestamp is >5 minutes older than the feed header timestamp, discard the update.
**Detection:** Look for "stationary" buses with high delays that never change over multiple polling cycles.

## Moderate Pitfalls

### Pitfall 1: Schedule Version Mismatch (Static vs. Real-time)
**What goes wrong:** Using an old `stop_times.txt` to calculate delays for a new GTFS-R feed after a service change (e.g., Seasonal re-scheduling).
**Prevention:** Check the `feed_info` or file hashes. Automate the re-ingestion of static GTFS whenever a new version is published.
**Phase Mapping:** Ingestion (Phase 1).

### Pitfall 2: Stop-Skipping Logic
**What goes wrong:** GTFS-R often only provides updates for the *next* few stops. If a bus skips a stop due to a detour, the system might assume it's "infinitely late" until it reappears.
**Prevention:** Use `SCHEDULE_RELATIONSHIP: SKIPPED` flags and ensure the distribution model can handle gaps in stop observations.
**Phase Mapping:** Analysis (Phase 3).

## Minor Pitfalls

### Pitfall 1: Timezone Complexity at Midnight
**What goes wrong:** Transit days often exceed 24 hours (e.g., a trip starting at 25:30:00). Naive `datetime` parsing will fail.
**Prevention:** Use a transit-aware time parser that handles HH > 23 relative to the service date.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Ingestion | Header vs. System Clock | Use `header.timestamp` for all calculations. |
| Storage | Data Volume Explosion | Implement TTL or partitioning in Postgres (TimescaleDB). |
| Analysis | Outlier Sensitivity | Use medians or percentiles (P50, P90) rather than mean for distributions. |
| Visualization | Misinterpreting "On Time" | Define "On Time" clearly (e.g., -1 to +5 mins) to match user expectations. |

## Sources

- [GTFS Realtime Best Practices](https://gtfs.org/realtime/best-practices/)
- [MobilityData: Common GTFS-RT Producer Errors](https://mobilitydata.org/)
- [Translink Developer API Documentation](https://developer.translink.ca/)
