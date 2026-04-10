---
phase: 01
plan: 03
subsystem: backend
tags: [kafka, delay-calculation, next-stop]
requires: [REL-01]
provides: [next-stop-delay-semantics]
affects: [delay_consumer.py, api.py]
tech-stack: [Python, MongoDB, GTFS-R]
key-files:
  modified: [delay_consumer.py, api.py]
decisions:
  - "Isolated the logical 'next stop' for each vehicle by picking the first stop_time_update after sorting by stop_sequence."
metrics:
  duration: 120s
  completed: 2026-04-10T02:56:00Z
---

# Phase 01 Plan 03: Backend Delay Refinement Summary

## Summary
Refined the backend delay calculation logic in `delay_consumer.py` to identify and persist the logical "next stop" for each vehicle. This ensures that delay data is stop-specific rather than a broad trip-level average. Also exposed the `next_stop_id` through the FastAPI `VehicleUpdate` model to enable stop-focused visualization in the frontend.

## Deviations from Plan
None - plan executed exactly as written.

## Known Stubs
None.

## Self-Check: PASSED
- [x] delay_consumer.py identifies next stop
- [x] delay_consumer.py persists next_stop_id
- [x] api.py exposes next_stop_id
