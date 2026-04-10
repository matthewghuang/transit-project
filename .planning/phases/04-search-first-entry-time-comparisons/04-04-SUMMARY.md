---
phase: 04-search-first-entry-time-comparisons
plan: 04
subsystem: ui
tags: [fastapi, react, postgres, recharts]

# Dependency graph
requires:
  - phase: 04-search-first-entry-time-comparisons
    provides: [04-03]
provides:
  - Improved search with route name support and prioritized stop ID matches
  - Cleaned up dashboard and hero UI in frontend
  - Robust arrival time logic handling missing data
  - Fixed visibility of delay distribution chart
affects: [05-next-phase]

# Tech tracking
tech-stack:
  added: []
  patterns: [Priority-based hero time selection, Route-aware stop search]

key-files:
  created: []
  modified: [api.py, frontend/src/components/StopDashboard.tsx, frontend/src/components/TimeTriad.tsx, frontend/src/components/DelayDistributionChart.tsx]

key-decisions:
  - "Modified search_stops to detect route names and return associated stops."
  - "Switched hero time selection to priority-based (Actual > Predicted > Scheduled) instead of minimum-based."
  - "Removed automatic fallbacks for actual/predicted times in API to allow UI to handle missing data explicitly."

patterns-established:
  - "Priority-based hero time: UI shows the 'best' available time source."

requirements-completed: ["SRCH-01", "SRCH-02", "SRCH-03", "UIO-01"]

# Metrics
duration: 15 min
completed: 2026-04-10T17:47:12Z
---

# Phase 4 Plan 4: Search & UI Gap Closure Summary

**Improved search precision with route-name support, streamlined dashboard UI, and fixed reliability chart visibility.**

## Performance

- **Duration:** 15 min
- **Started:** 2026-04-10T09:00:00Z
- **Completed:** 2026-04-10T17:47:12Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments
- **Route-aware Search:** Searching for "R5" now correctly returns stops serving that route by checking GTFS route metadata.
- **ID Prioritization:** Exact stop ID matches (e.g., "50959") are now weighted to appear first in search results.
- **Clean Dashboard:** Removed the redundant informational card and simplified hero indicators for a more focused UI.
- **Reliability Fix:** Ensured the delay distribution chart is visible in expanded view by providing a minimum height container.

## Task Commits

Each task was committed atomically:

1. **Task 1: Improve API Search & Arrival Logic** - `8928116` (feat)
2. **Task 2: Clean up Frontend Dashboard & Hero UI** - `c3573f4` (feat)
3. **Task 3: Fix PDF Chart (DelayDistributionChart) Visibility** - `a3ba6fe` (feat)

**Plan metadata:** `pending` (docs: complete plan)

## Files Created/Modified
- `api.py` - Added route-based search and fixed arrival time fallbacks.
- `frontend/src/components/StopDashboard.tsx` - Removed redundant info section.
- `frontend/src/components/TimeTriad.tsx` - Improved hero time logic and chart container.

## Decisions Made
- Used in-memory `routes_lookup` for fast route-name-to-id mapping in search.
- Decided to return `null` for missing arrival data to allow clear UI state (e.g., "--:--:--") instead of misleading scheduled times.

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
None.

## Next Phase Readiness
Phase 4 gap closure complete. The search and dashboard are now robust enough for production-like reliability visualization. Ready for next phase.

---
*Phase: 04-search-first-entry-time-comparisons*
*Completed: 2026-04-10*
