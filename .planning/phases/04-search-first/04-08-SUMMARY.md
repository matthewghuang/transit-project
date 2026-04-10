---
phase: 04-search-first
plan: 08
subsystem: api
tags: [fix, gtfs, stop-resolution]
requires: ["SRCH-04", "UIO-01"]
provides: ["stop_code to stop_id resolution"]
affects: ["api.py"]
tech-stack:
  added: []
  patterns: ["In-memory dictionary mapping"]
key-files:
  created: []
  modified: ["api.py"]
key-decisions:
  - "Use an in-memory dictionary `stop_code_to_id` for fast resolution during request handling."
  - "Resolved stop_id at the entry point of sensitive endpoints (next_buses, distribution) to ensure compatibility with both internal IDs and public stop codes."
requirements-completed: ["SRCH-04", "UIO-01"]
duration: 8 min
completed: 2026-04-10T18:36:30Z
---

# Phase 04 Plan 08: Stop Code Resolution Summary

## Summary
Fixed the "--:--:--" display issue by implementing a robust stop_code to stop_id resolution layer in the API. This ensures that when a user searches for a stop using its 5-digit code (e.g., 50959), the API correctly maps it to the internal GTFS stop_id (e.g., 968) before querying real-time and historical data.

## Accomplishments
- **Implemented stop_code_to_id mapping:** Added a global dictionary in `api.py` populated during startup from `stops.txt`.
- **Enriched Load Logic:** Updated `load_stops()` to handle `stop_code` extraction and handle cases where it might be missing.
- **Integrated Resolution:** Modified `get_next_buses` and `get_delay_distribution` endpoints to resolve stop codes automatically at the beginning of the request lifecycle.
- **Verified Fix:** Confirmed via curl that searching for stop code `50959` returns valid scheduled and predicted times for stop `968`.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED
- [x] Created files exist: N/A (modified api.py)
- [x] Commits exist: 875fbe6, 8f79dcc
- [x] API verification passed for stop code 50959
