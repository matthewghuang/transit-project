# Phase 5: Advanced Reliability Insights - Context

**Gathered:** 2026-04-10
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase enhances the analytical depth of the dashboard. It moves beyond simple delay distributions to provide actionable "Reliability Insights." This includes:
1. **Confidence Windows:** Recommending arrival times based on a 95% certainty threshold.
2. **Ghost Bus Detection:** Identifying and flagging real-time updates that have gone stale.
3. **Cancellation Analysis:** Tracking and visualizing historical trip cancellations.

</domain>

<decisions>
## Implementation Decisions

### Confidence Windows
- **D-01: Arrive-By Logic.** The system should calculate a "Conservative Arrive-By" time. If a route has high variance, the Arrive-By time will be significantly earlier than the scheduled time.
- **D-02: 95% Threshold.** By default, use the 95th percentile of historical arrivals for the reliability window.

### Ghost Bus Detection
- **D-03: Stale Update Threshold.** Vehicles that haven't updated their position or ETA in more than 5 minutes should be flagged as "Ghost Buses" (potentially missing or GPS-failure).
- **D-04: UI Indicator.** Ghost buses should appear with a "Stale Data" or "GPS Lost" warning in the Time Triad.

### Cancellation Analysis
- **D-05: Historical Logging.** The system must log when a trip is explicitly marked as `CANCELED` in the GTFS-R feed to distinguish between "Late" and "Never Came."

### the agent's Discretion
- Exact visual treatment of the "Ghost Bus" warning.
- Logic for handling stops with very low historical data (fallback to schedule-only or a wider global average).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Transit Data Specs
- `google_transit/` — GTFS-R spec for `TripUpdate` and `VehiclePosition`.
- `.planning/REQUIREMENTS.md` — Specifically ADV-01, ADV-02, and ADV-03.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `TimeTriad.tsx`: Will be the primary host for the "Arrive-By" recommendation and Ghost Bus warnings.
- `DelayDistributionChart.tsx`: Can be updated to visually highlight the 95% confidence region on the PDF curve.
- Backend PDF Logic: The existing KDE/PDF calculation in the FastAPI backend will be extended to return specific percentiles.

### Integration Points
- Backend: `GET /api/reliability/{stop_id}/{route_id}` — New endpoint or extension of existing probabilistic API.
- Frontend: `useNextBuses.ts` needs to handle the `is_stale` flag for Ghost Bus detection.

</code_context>

<specifics>
## Specific Ideas

- "Commuters should know exactly when they *must* be at the stop to not miss the bus 19 times out of 20."

</specifics>

<deferred>
## Deferred Ideas

- **Predictive Traffic Integration:** Real-time road congestion data remains out of scope.

</deferred>

---

*Phase: 05-advanced-reliability-insights*
*Context gathered: 2026-04-10*
