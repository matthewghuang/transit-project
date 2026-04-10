---
phase: 04-search-first
plan: 09
subsystem: API/Frontend
tags: ["stop-codes", "search", "UI"]
requires: ["04-08"]
provides: ["Consistent stop_code display"]
affects: ["api.py", "HeroSearch.tsx", "StopDashboard.tsx"]
tech-stack:
  added: []
  patterns: ["id-mapping"]
key-files:
  created: []
  modified: ["api.py", "frontend/src/components/HeroSearch.tsx", "frontend/src/components/StopDashboard.tsx"]
key-decisions:
  - "Prefer stop_code over stop_id for public-facing identifiers to improve user familiarity."
  - "Maintain internal stop_id resolution in the backend for data consistency."
requirements-completed: ["SRCH-01", "SRCH-04"]
duration: 5 min
completed: "2026-04-10T18:48:06Z"
---

# Phase 04 Plan 09: Fix Conflicting IDs Summary

Ensured consistent use of 5-digit stop codes for display in search results and the dashboard header, while maintaining internal data integrity.

## Key Changes

### Backend (api.py)
- Updated `load_stops()` to build an `id_to_stop_code` mapping for reverse lookups.
- Modified `search_stops` to select `stop_code` from the database and use it as the `id` in the response if available.
- Updated `get_stops` to also return the `stop_code` as the `id`.
- Modified `get_delay_distribution` and `get_next_buses` to resolve input codes to internal IDs for lookup, but return the original input ID back to the client for state consistency.

### Frontend
- Verified `HeroSearch.tsx` correctly displays the ID returned from the API (now the stop code) with a '#' prefix.
- Verified `StopDashboard.tsx` uses the provided `stopId` (now the code) in the header.

## Deviations from Plan

None - plan executed exactly as written.

## Verification Results

1.  **Stop Code Resolution:** Verified that `api.py` correctly maps stop codes to internal IDs for data fetching.
2.  **API Search Response:** `curl http://localhost:8000/api/stops/search?q=50959` returns `"id": "50959"`.
3.  **Frontend Display:** Search results and dashboard header now show the familiar 5-digit code.

## Commits
- `79fb5bb`: feat(04-09): Update Backend to Prefer stop_code for Display
- `3e91ddb`: docs(04-09): Add debug documentation for stop code conflict

## Self-Check: PASSED
