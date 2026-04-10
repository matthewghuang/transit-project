# Phase 1: Real-time Data Foundation - Context

**Gathered:** April 09, 2026
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish the core ingestion pipeline that calculates discrete delay metrics by joining real-time vehicle positions/trip updates with static schedules. Deliver a user-facing stop-focused UI that shows real-time lateness in map popups.

</domain>

<decisions>
## Implementation Decisions

### Static Data Ingestion
- **D-01:** Use an **In-Memory Dictionary** to store the schedule. Load a mapping of `{ (trip_id, stop_id): scheduled_arrival_time }` from `stop_times.txt` into the consumer's memory on startup for O(1) lookups.
- **D-02:** Use **Pandas** for the initial parse of `google_transit/*.txt` files, consistent with established patterns in `demo_consumer.py`.

### Delay Calculation
- **D-03:** Operate in **Strict Mode**. Only record and display a delay if the GTFS-Realtime message explicitly contains a `stop_time_update` with an arrival delay. This ensures the "distribution" data is grounded in agency-provided truth rather than geometric estimation.
- **D-04:** Use `header.timestamp` from the feed as the temporal anchor for all lateness calculations to avoid system clock drift bias.

### Frontend Presentation
- **D-05:** Use **Map Popups** as the primary UI for stop-focused info. Clicking a stop on the Leaflet map should display a popup containing the real-time countdown and "Lateness" status for incoming vehicles.
- **D-06:** Maintain the existing **Zustand** state management pattern for selected stops and filtered positions.

### Integration Point
- **D-07:** Implement as a **New Parallel Consumer** (`delay_consumer.py`). This keeps the analytical ingestion decoupled from the simple position-tracking consumer.

### the agent's Discretion
- Exact data structure of the in-memory schedule cache (e.g. nested dicts vs tuple-keys).
- Styling of the map popups (colors, fonts), following the modern/minimal aesthetic of the existing app.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Scope
- `.planning/PROJECT.md` — Project vision and core value.
- `.planning/REQUIREMENTS.md` — v1 requirements (CORE-01, CORE-02, CORE-03, REL-01).

### Codebase Patterns
- `.planning/codebase/ARCHITECTURE.md` — Layer definitions and data flow.
- `.planning/codebase/CONVENTIONS.md` — Naming and styling standards.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `google_transit/` folder contains all required static GTFS files.
- `main.py` provides the Kafka producer logic.
- `frontend/src/components/Map.tsx` and `frontend/src/stores/filterStore.ts` are the primary anchors for UI work.

### Established Patterns
- Python consumers use `confluent-kafka` and `gtfs_realtime_pb2`.
- MongoDB TTL indexing for real-time snapshots (though Phase 1 primarily focuses on the ingestion logic).

### Integration Points
- Kafka topic `position` (or a dedicated `trip_update` topic if `main.py` is updated to poll the realtime URL).

</code_context>

<specifics>
## Specific Ideas

- "I want to be able to see the distribution... but for Phase 1, just showing the current lateness clearly on the map is the win."
- "The join is the bottleneck — keep it fast."

</specifics>

<deferred>
## Deferred Ideas

- Persistent storage in PostgreSQL/TimescaleDB — Phase 2.
- KDE/Probability Distribution charts — Phase 3.

</deferred>

---

*Phase: 01-real-time-data-foundation*
*Context gathered: April 09, 2026*
