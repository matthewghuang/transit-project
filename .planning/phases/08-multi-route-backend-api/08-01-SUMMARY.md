---
phase: "08"
plan: "01"
subsystem: api
tags: [fastapi, python, gtfs, transit]

# Dependency graph
requires:
  - phase: "07"
    provides: ["Probability distribution API", "Single-bus arrival endpoint"]
provides:
  - "Multi-route arrival API endpoint (/api/stops/{id}/next_buses)"
  - "In-memory trip-to-route mapping"
  - "Route-aware GTFS stop_times lookup"
affects: ["Phase 09: Horizontal Carousel UI"]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Multi-route collection in single API request", "GTFS enrichment via trip_to_route mapping"]

key-files:
  created: []
  modified: ["api.py"]

key-decisions:
  - "Refactored next_buses endpoint to return one arrival per unique route serving the stop."
  - "Integrated trip_to_route mapping into load_stop_times for O(1) route lookup per stop time."

requirements-completed: [MULT-01]

# Metrics
duration: 2min
completed: 2026-04-10
---

# Phase 08 Plan 01: Multi-Route Backend API Summary

**Updated the `/api/stops/{id}/next_buses` endpoint to return a sorted list of next arrivals for all unique routes at a stop, supporting the Phase 09 carousel UI.**

## Performance

- **Duration:** 2 min
- **Started:** 2025-04-10T21:05:11Z
- **Completed:** 2025-04-10T21:07:29Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Refactored `api.py` to associate every stop time with its `route_id` by loading `trips.txt` into memory.
- Updated `NextBusesResponse` schema to include `route_id` and `route_name`.
- Implementation of the multi-route logic in the `/api/stops/{stop_id}/next_buses` endpoint, which now finds the first upcoming bus for each route serving the stop.
- Response is sorted chronologically by `scheduled_time`, allowing the frontend to easily display the most imminent arrivals first.

## Task Commits

Each task was committed atomically:

1. **Task 1: Enrich GTFS lookups with route_id** - `d7b0b28` (feat)
2. **Task 2: Refactor API to return unique route arrivals** - `647b8b5` (feat)

**Plan metadata:** `pending` (docs: complete plan)

## Files Created/Modified
- `api.py` - Updated to support multi-route GTFS lookups and the refactored next_buses endpoint.

## Decisions Made
- **Early Route Enrichment:** Decided to map `trip_id` to `route_id` during the static load phase (`load_stop_times`) rather than at request time to maintain low API latency.
- **D-05 Safety Cap:** Maintained the safety cap for `arrive_by_time` across all routes.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- **Process Lock:** Port 8000 was held by an old API process during verification. Resolved by identifying and killing the process with `lsof` and `kill`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Backend is now ready to serve multiple arrivals per stop.
- Ready for Phase 09: Multi-Bus Stop Carousel UI.

---
*Phase: 08-multi-route-backend-api*
*Completed: 2026-04-10*
