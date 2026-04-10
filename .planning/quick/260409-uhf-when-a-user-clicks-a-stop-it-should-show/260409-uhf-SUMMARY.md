---
phase: quick
plan: 01
subsystem: ui-api
tags:
  - next-buses
  - prediction
  - historical-delay
dependency_graph:
  requires:
    - active_vehicles
    - delay_observations
    - stop_times.txt
  provides:
    - /api/stops/{stop_id}/next_buses
    - NextBusesDisplay component
  affects:
    - stop popup UI
tech_stack:
  added: []
  patterns:
    - React hook data fetching
    - FastAPI route
key_files:
  created:
    - frontend/src/hooks/useNextBuses.ts
    - frontend/src/components/NextBusesDisplay.tsx
  modified:
    - api.py
    - frontend/src/components/Map.tsx
decisions:
  - Load stop_times.txt directly into memory at startup (fast ~3s parsing) to provide ultra-low latency lookups without needing a heavy database for static times.
metrics:
  duration: 10m
  completed_date: "2026-04-10"
---

# Phase Quick Plan 01: Next Buses Summary

Enhanced stop click popup to display scheduled, actual, and predicted times for the next bus.

## Plan Execution Status

- **Status:** COMPLETED
- **Tasks Completed:** 2/2
- **Remaining Tasks:** 0

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None

## Self-Check: PASSED
FOUND: api.py
FOUND: frontend/src/hooks/useNextBuses.ts
FOUND: frontend/src/components/NextBusesDisplay.tsx
