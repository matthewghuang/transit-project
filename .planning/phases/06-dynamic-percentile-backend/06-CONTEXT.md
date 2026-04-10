# Phase 6: Dynamic Percentile Backend - Context

**Gathered:** 2026-04-10
**Status:** Ready for planning

<domain>
## Phase Boundary

Backend safely computes and enforces dynamic confidence-based delay distributions. The API will accept a confidence parameter and return adjusted arrival recommendations that are never later than the scheduled time.

</domain>

<decisions>
## Implementation Decisions

### Percentile Granularity
- **D-01:** The API will support discrete percentile steps: 50, 75, 90, 95, and 99.
- **D-02:** Requests for unsupported percentiles will be snapped to the nearest discrete step.

### Calculation Method
- **D-03:** Use approximate aggregates (TimescaleDB `percentile_agg`) for performance and scalability, avoiding expensive O(N log N) exact sorts.

### Low Data Strategy
- **D-04:** Results with fewer than 10 historical observations must be flagged with a "low_confidence" warning in the API response.

### Arrive-By Safety (Prior Decision)
- **D-05:** All arrive-by recommendations must be capped to ensure they are never later than the scheduled time: `min(scheduled, predicted)`.

### the agent's Discretion
- Exact JSON structure for the low-confidence flag.
- SQL query optimization for the discrete percentile steps.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Core Logic
- `.planning/REQUIREMENTS.md` — Requirement CORE-04 (dynamic percentiles) and CORE-05 (safety caps).
- `api.py` — Current implementation of `/api/distribution` and `/api/stops/{stop_id}/next_buses`.

[No external specs — requirements fully captured in decisions above]

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `api.py`: Existing `NextBusesResponse` and `DistributionResponse` models.
- `db_init.py`: Existing schema for `delay_observations` hypertable.

### Established Patterns
- FastAPI routes with Pydantic validation.
- `asyncpg` for database interaction.
- `numpy` used for in-memory statistics (to be replaced by DB-side approximate aggregates).

### Integration Points
- `/api/stops/{stop_id}/next_buses`: Update to accept `confidence` query param.
- `/api/distribution/{stop_id}`: Update to return dynamic percentiles based on provided param.

</code_context>

<specifics>
## Specific Ideas

- "Commuters should never miss a bus because the app said it was 10 minutes late when it was actually on time."
- Use discrete steps to allow future caching layer (e.g., Redis) if volume increases.

</specifics>

<deferred>
## Deferred Ideas

- Plain-English labels (e.g., "Living Dangerously" for 50%) — Phase 7/v2.
- Chart highlighting — Phase 7.

</deferred>

---

*Phase: 06-dynamic-percentile-backend*
*Context gathered: 2026-04-10*
