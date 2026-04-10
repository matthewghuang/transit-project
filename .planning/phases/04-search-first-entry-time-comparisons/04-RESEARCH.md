# Phase 4 Research: Search-First Entry & Time Comparisons

## Summary
Transitioning to a search-centric UI requires a robust fuzzy search backend, removal of Leaflet map dependencies, and a new "Time Triad" dashboard layout.

## Technical Findings

### Fuzzy Search Implementation
- **Backend:** PostgreSQL `pg_trgm` extension is recommended for fuzzy matching on `stop_name` in `stops.txt`.
- **Query:** `SELECT stop_id, stop_name FROM stops WHERE stop_name % $1 OR stop_id = $1 ORDER BY similarity(stop_name, $1) DESC LIMIT 10`.
- **Numeric search:** Direct `stop_id` lookup should bypass fuzzy matching for speed (as per D-03).

### UI Refactoring
- **Map Removal:** `frontend/src/components/Map.tsx` and all imports of `leaflet` in `package.json` should be removed.
- **State:** `filterStore.ts` needs to be purged of `bounds` or `mapCenter` logic.
- **Dashboard:** The new dashboard will consume `GET /api/stops/{stop_id}/next_buses` which already provides Scheduled/Actual/Predicted times.

### Time Triad Logic
- **Hero Time:** Calculated on frontend as `min(scheduled, actual, predicted)`.
- **Expansion:** Use standard React state (`isExpanded`) to toggle between Hero view and Triad view.
- **Probability Curve:** Re-use `DelayDistributionChart.tsx` (from Phase 3) in the expanded view.

## Validation Architecture

### Verification Strategy
- **Automated:** 
  - Backend: `pytest` for `/api/stops/search` with various inputs (intersection, ID, partial match).
  - Frontend: `npm test` (if exists) or manual verification of map removal via bundle analysis.
- **Manual:**
  - Verify Hero Time selection logic (earliest of three).
  - Verify Recent Searches persist in localStorage.

## Common Pitfalls
- **Performance:** Fuzzy searching 10,000+ stops on every keystroke can be slow. Debouncing (300ms) and indexing are critical.
- **GTFS Variations:** Intersections in `stops.txt` often use "at", "&", "and", or "/" — `pg_trgm` handles these better than standard `LIKE`.

