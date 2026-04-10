# Phase 2: Historical Storage & Infrastructure - Context

**Gathered:** April 09, 2026
**Status:** Ready for planning

<domain>
## Phase Boundary

Persist delay observations in a scalable time-series database optimized for longitudinal analysis. Migrate the real-time state from MongoDB to PostgreSQL/TimescaleDB to consolidate the storage layer.

</domain>

<decisions>
## Implementation Decisions

### Database Setup
- **D-01:** Use **TimescaleDB via Docker**. Update `docker-compose.yml` to include the `timescale/timescaledb:latest-pg17` image.
- **D-02:** Use **SQLAlchemy** or raw `asyncpg` for database interactions, ensuring async compatibility with the consumer loop.

### Persistence Pattern
- **D-03:** Implement **Batch Inserts**. The `delay_consumer.py` will accumulate observations in memory and flush them to the database in batches (e.g., every 10 seconds or 100 records) to maximize write throughput.
- **D-04:** Observations will include: `timestamp` (anchored to feed time), `stop_id`, `trip_id`, `route_id`, and `delay_seconds`.

### Aggregation & Retention
- **D-05:** Use **Continuous Aggregates**. Set up TimescaleDB continuous aggregates to pre-calculate delay metrics (mean, median, p95) bucketed by hour and day-of-week.
- **D-06:** Retention: Keep raw observations for 30-90 days (TBD based on storage growth) while keeping aggregated summaries indefinitely.

### Migration
- **D-07:** **Migrate to SQL**. Phase out MongoDB. The real-time vehicle positions and "Next Stop" data will now be stored in a dedicated SQL table (e.g., `active_vehicles`) with indices optimized for real-time API lookups.

### the agent's Discretion
- Table schema design (naming, types, constraints).
- Exact batch size and flush interval tuning.
- The specific SQL migration path for `demo_consumer.py` (if it should also be updated or just superseded).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Scope
- `.planning/PROJECT.md` — Project vision and core value.
- `.planning/REQUIREMENTS.md` — v1 requirements (REL-02).
- `.planning/research/STACK.md` — Prescriptive stack choices (TimescaleDB hyperfunctions).

### Codebase Patterns
- `.planning/phases/01-real-time-data-foundation/01-CONTEXT.md` — Previous decisions on ingestion and delay calculation.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docker-compose.yml` provides the infrastructure template.
- `delay_consumer.py` (created in Phase 1) provides the ingestion logic and schedule join.

### Established Patterns
- Python consumers in this project are transitioning from MongoDB to SQL.
- Batching is a new pattern for this codebase but aligns with high-velocity transit data needs.

### Integration Points
- `docker-compose.yml` for database service.
- `delay_consumer.py` for database write logic.

</code_context>

<specifics>
## Specific Ideas

- "Consolidate the stack. MongoDB served its purpose for the demo, but Timescale is the future here."
- "Batching is critical for the 30s poll frequency to avoid locking up the DB."

</specifics>

<deferred>
## Deferred Ideas

- KDE/Probability Distribution API endpoints — Phase 3.
- Charting and Frontend dashboard — Phase 3.

</deferred>

---

*Phase: 02-historical-storage-infrastructure*
*Context gathered: April 09, 2026*
