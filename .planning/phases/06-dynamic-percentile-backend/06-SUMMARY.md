# Phase 6 Plan 1: Dynamic Percentile Backend Summary

## Summary
- Implemented dynamic confidence percentiles for bus delay distributions.
- Added an "Arrive-By" safety cap to ensure recommendations are never later than the scheduled time.
- Updated the API to return a `low_confidence` flag when data is sparse (<10 observations).
- Integrated discrete percentile snapping (50, 75, 90, 95, 99) for better cacheability and consistency.

## Tech Stack
- FastAPI (Query parameters, Pydantic models)
- PostgreSQL (PERCENTILE_CONT for distribution calculation)

## Key Files
- `api.py`: Updated endpoints and models.

## Deviations from Plan
### [Rule 3 - Blocking Issue] TimescaleDB `percentile_agg` missing
- **Found during:** Verification (Task 2)
- **Issue:** The `percentile_agg` hyperfunction was not available in the current PostgreSQL environment despite TimescaleDB being installed.
- **Fix:** Switched to standard PostgreSQL `PERCENTILE_CONT` within a `WITHIN GROUP (ORDER BY ...)` clause.
- **Impact:** Negligible for current data volumes; provides exact rather than approximate results.
- **Commit:** f814798

## Self-Check: PASSED
- [x] API accepts confidence parameter.
- [x] Arrive-by time is correctly capped: `min(scheduled, predicted)`.
- [x] `low_confidence` flag appears in sparse data scenarios.
- [x] Discrete percentile snapping works as expected.
