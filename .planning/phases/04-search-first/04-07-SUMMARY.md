---
phase: 04-search-first
plan: 07
subsystem: backend
tags: [timescaledb, stateful, gtfs-realtime, api]
requires: ["04-06"]
provides: ["trip_delays state"]
affects: ["api.py", "delay_consumer.py", "db_init.py"]
tech-stack:
  added: []
  patterns: ["Stateful trip delay tracking"]
key-files:
  created: []
  modified: ["db_init.py", "delay_consumer.py", "api.py"]
key-decisions:
  - "Introduced trip_delays table as a stateful cache for the latest known delay of every active trip, resolving the 'sparse data' issue in the Time Triad."
requirements-completed: ["UIO-04"]
duration: 1 min
completed: 2026-04-10T18:15:55Z
---

# Phase 04 Plan 07: Fix Actual Time Missing Summary

## Summary

Implemented a stateful trip delay tracking system to fix the "Actual arrival time missing" issue in the Time Triad. By introducing a dedicated `trip_delays` table that tracks the latest known delay for every active trip across all its stops, we ensure that the API can consistently provide real-time arrival estimates even if the specific stop wasn't the primary focus of the latest GTFS-R update.

## Key Changes

### Database
- Added `trip_delays` table to `db_init.py` with `trip_id` as primary key to store current trip state.

### Consumer
- Updated `delay_consumer.py` to upsert every trip update into the `trip_delays` table, maintaining a fresh view of all active trip delays.

### API
- Modified the `/api/stops/{stop_id}/next_buses` endpoint in `api.py` to prioritize the `trip_delays` table for "Actual" time calculations, significantly increasing the reliability of real-time data delivery to the UI.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED

- [x] `db_init.py` modified and run successfully.
- [x] `delay_consumer.py` updated with upsert logic.
- [x] `api.py` query updated to use `trip_delays`.
- [x] Commits made for each task.

## Commits
- cf52a97: feat(04-07): add trip_delays table to database initialization
- 0560eda: feat(04-07): update delay_consumer.py to upsert trip_delays
- 848514f: feat(04-07): update api.py to use trip_delays for Actual time
