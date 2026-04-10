# Phase 8: Multi-Route Backend API - Context

**Gathered:** 2026-04-10
**Status:** Ready for planning

<domain>
## Phase Boundary

Update the backend API to support stops served by multiple routes. The `/api/stops/{id}/next_buses` endpoint must transition from returning a single bus to returning an array of the next upcoming buses for every unique route at the stop.

</domain>

<decisions>
## Implementation Decisions

### Response Structure
- **D-01:** The API will return an array of arrival objects rather than a single object.
- **D-02:** Each object in the array will contain the full "Time Triad" data (scheduled, actual, predicted, arrive-by) for that specific bus.

### Route Selection & Uniqueness
- **D-03:** The API will return exactly one upcoming bus for every unique `route_id` serving the stop.
- **D-04:** Uniqueness is defined by `route_id` (GTFS standard). 

### Sorting
- **D-05:** Results will be sorted chronologically by `scheduled_time` to ensure the most imminent arrivals appear first in the carousel.

### the agent's Discretion
- **D-06:** Choice of Pydantic model refactoring (e.g., `NextBusesResponse` containing a list vs. returning a naked list).
- **D-07:** Performance optimization for joining `stop_times` with `trips` to extract `route_id`.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### API & Models
- `api.py` — Existing endpoint implementation and Pydantic models.

### Data Schema
- `google_transit/stop_times.txt` — Static schedule data.
- `google_transit/trips.txt` — Mapping between `trip_id` and `route_id`.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `stop_times_lookup` (api.py): Already contains parsed schedule data; needs enhancement to include `route_id`.
- `NextBusesResponse` (api.py): Existing Pydantic model that needs to be adapted for multi-route lists.

### Established Patterns
- In-memory lookups for GTFS static data to maintain ultra-low latency.
- Async database calls for real-time delay data.

### Integration Points
- `/api/stops/{stop_id}/next_buses`: The specific endpoint being refactored.

</code_context>

<specifics>
## Specific Ideas

- "Each stop can have 1 or more busses. I want to display each bus in a card in a mobile-friendly carousel view."
- The goal is to provide a "swipeable" experience on the frontend (to be implemented in Phase 9).

</specifics>

<deferred>
## Deferred Ideas

- **Phase 9: Swipeable Carousel UI** — All frontend implementation of the carousel.
- **Directional Filtering** — Ability to filter the carousel by direction (out of scope for Phase 8).

</deferred>

---

*Phase: 08-multi-route-backend-api*
*Context gathered: 2026-04-10*
