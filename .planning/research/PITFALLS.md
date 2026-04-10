# Domain Pitfalls

**Domain:** Transit Reliability Visualization (Interactive Features & Dynamic Percentiles)
**Researched:** April 10, 2026

## Critical Pitfalls (v1.2 Interactive Confidence Milestone)

Mistakes that cause rewrites or major issues when adding dynamic confidence sliders and percentile APIs.

### Pitfall 1: On-the-fly SQL Percentile Calculation (DB Meltdown)
**What goes wrong:** Dragging the confidence slider causes severe API lag and database CPU spikes.
**Why it happens:** PostgreSQL's exact percentile function (`percentile_cont`) is an ordered-set aggregate requiring sorting of the entire dataset for every query. Running this dynamically per-request over millions of historical delay rows is O(N log N).
**Consequences:** Unusable, non-responsive interactive slider and systemic database latency.
**Prevention:** 
- **DB Level:** Use TimescaleDB Toolkit's `percentile_agg` and `approx_percentile` for hyper-fast approximations.
- **Architecture Level:** Fetch a pre-calculated bucketing (histogram/CDF) *once* per stop/route on load, and have the React frontend calculate the specific percentiles dynamically as the slider moves.

### Pitfall 2: Slider Event Spamming (API Throttling)
**What goes wrong:** The frontend fires dozens of API requests per second while the user is dragging the slider.
**Why it happens:** Binding API fetches directly to the React `onChange` event of a range input without debouncing.
**Consequences:** Race conditions (responses arrive out of order, UI flickers), backend rate limits hit, unnecessary load.
**Prevention:** Use an `onChangeEnd` (or `onMouseUp`/`onTouchEnd`) event for API calls, or implement a 300ms debounce. Ideally, calculate percentiles client-side using cached data so the slider updates UI instantly without network calls.

### Pitfall 3: "Conservative" Over-Correction Logic
**What goes wrong:** The app tells users to arrive extremely early, destroying trust and usability.
**Why it happens:** The milestone requires recommendations to *never* be later than the scheduled time. If a route is chronically 10 minutes late, a strict "subtract the 95th percentile delay from schedule" logic might tell the user to arrive 10 minutes *before* the schedule.
**Prevention:** Clearly separate "Predicted Arrival Time" (which should reflect the actual expected lateness curve) from the "Arrive-By/Departure Recommendation." The arrive-by time should cap at the scheduled time (to catch early buses) but shouldn't arbitrarily subtract late variance from the schedule.

### Pitfall 4: Ignoring Negative Delays (Early Departures)
**What goes wrong:** The confidence window fails to account for buses that arrive *before* the scheduled time.
**Why it happens:** Assuming "delay" is bounded at 0. A 90% confidence window might only look at the top 90% of lateness, ignoring the bottom 10% of early departures which are actually the highest risk for missing the bus.
**Prevention:** Ensure the lower bound of the confidence interval captures early arrivals (e.g., analyzing the 5th to 95th percentiles, not just 0 to 90th).

## Legacy Pitfalls (v1.0 GTFS-R Ingestion)

### Pitfall 1: Clock Drift and Timestamp Misalignment
**Prevention:** Always use the `header.timestamp` from the feed as the reference point for "current" time. Synchronize processing servers via NTP.

### Pitfall 2: Handling Trip Cancellations as "Missing Data"
**Prevention:** Implement a "Dead Man's Switch" for trips. If a trip is in the static schedule but flagged as `CANCELED` in the feed, record it as a "canceled" event.

### Pitfall 3: The "Ghost Bus" (Stale Data) Problem
**Prevention:** Validate the `timestamp` on individual `TripUpdate` or `VehiclePosition` entities. If >5 minutes older than header, discard.

## Phase-Specific Warnings (v1.2)

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| API Update | DB sorting overload | Compute distributions client-side or use Timescale approximate aggregates. |
| Slider UI | Event spam | Debounce slider changes or decouple API from dragging state. |
| Recommendation Logic | Confusing arrive-by times | Baseline the "safe" time at the scheduled time, but display the full late curve. |

## Sources

- [TimescaleDB Documentation on approximate percentiles] - HIGH confidence
- [React Performance Best Practices (Debouncing/Throttling)] - HIGH confidence
- [GTFS Realtime Best Practices](https://gtfs.org/realtime/best-practices/)
