# Phase 3: Probabilistic API & Visualization - Context

**Gathered:** April 09, 2026
**Status:** Ready for planning

<domain>
## Phase Boundary

Transform raw historical delay observations into actionable probabilistic insights. Deliver a FastAPI statistical endpoint and a React-based distribution dashboard that visualizes arrival likelihoods via area-shaded histograms.

</domain>

<decisions>
## Implementation Decisions

### Statistical Engine
- **D-01:** Use **Simple Histograms** for the underlying distribution data. Bucket delay observations into 1-minute intervals. This provides a transparent, easy-to-reason-about likelihood model.
- **D-02:** Use **NumPy** for server-side bucketing and density calculation.

### Temporal Windowing
- **D-03:** Use **Slot-based filtering**. Distributions will be derived from observations within a 2-hour window centered on the current time (or target scheduled time), partitioned by day-of-week type (Weekday vs. Weekend).

### Frontend Visualization
- **D-04:** Use an **Area Chart** to render the distribution. The histogram buckets should be plotted as a continuous area curve (shaded underneath) to clearly communicate "probability mass" to the user.
- **D-05:** Use **Recharts** or a similar React charting library that aligns with the existing project's modern component architecture.

### Summary Statistics
- **D-06:** Use the **Median** as the "Typical Delay" metric. Display strings like "Usually arrives +2m late" to provide a resilient, non-skewed estimate of typical performance.

### the agent's Discretion
- Choice of specific React charting library (Recharts vs Victory vs Chart.js).
- Exact API response schema (e.g. array of bucket objects vs two parallel arrays).
- Visual styling of the area chart (colors, opacity, axis labels).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Scope
- `.planning/PROJECT.md` — Project vision and core value.
- `.planning/REQUIREMENTS.md` — v1 requirements (REL-03, REL-04).

### Codebase Patterns
- `.planning/codebase/ARCHITECTURE.md` — Layer definitions.
- `.planning/phases/02-historical-storage-infrastructure/02-CONTEXT.md` — Decisions on SQL schema and continuous aggregates.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `api.py` provides the framework for adding new FastAPI endpoints.
- `frontend/src/components/` is the location for the new distribution component.
- `TimescaleDB` (set up in Phase 2) provides the source data via SQL queries.

### Established Patterns
- Async API calls in Python using `asyncpg`.
- Zustand for frontend state management.

### Integration Points
- `/api/distribution/{stop_id}` endpoint.
- Map popups (from Phase 1) will trigger or host the distribution chart.

</code_context>

<specifics>
## Specific Ideas

- "I want the user to see a 'cloud' of probability. The area chart makes it obvious where the bus is most likely to be."
- "The histogram keeps it grounded in reality — no SciPy magic required yet."

</specifics>

<deferred>
## Deferred Ideas

- Buffer time recommendations ("Arrive by X") — Phase 4/v2.
- Multi-stop reliability comparison — v2.

</deferred>

---

*Phase: 03-probabilistic-api-visualization*
*Context gathered: April 09, 2026*
