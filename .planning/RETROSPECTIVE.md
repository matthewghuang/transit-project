# Project Retrospective: Translink Delay Distribution Dashboard

This living document captures lessons, patterns, and reflections across milestones to improve future execution.

## Milestone: v1.0 — Foundation & Probabilistic Insights

**Shipped:** 2026-04-10
**Phases:** 3 | **Plans:** 9

### What Was Built
- Multi-feed GTFS-R producer fetching positions and trip updates.
- Real-time delay engine joining live feeds with 90MB static `stop_times.txt`.
- TimescaleDB time-series storage with automated schema initialization.
- Probabilistic API providing stop-specific delay distributions.
- Frontend dashboard with interactive map, stop selection, and Recharts distribution curves.

### What Worked
- **Goal-backward planning:** Starting with the PDF visualization requirement forced the early implementation of the complex schedule join.
- **In-memory indexing:** Using pandas for the static schedule lookup proved extremely fast and avoided database load for real-time enrichment.
- **Docker-based DB init:** Moving the schema setup into a dedicated container resolved race conditions between the database and the ingestion services.

### What Was Inefficient
- **Late DB Migration:** Starting with MongoDB only to migrate to TimescaleDB in Phase 2 caused significant rework in the consumer and API. Choosing the final storage engine earlier would have saved 2 plans.
- **Mock Data Dependency:** Using mock stops in the frontend early on allowed for UI progress but required a second pass to wire up the real stop-approaching logic.

### Patterns Established
- **Service Resilience:** Implementing `wait_for_db` retry loops in all backend services.
- **Contextual Visualization:** Embedding complex statistical charts directly into map popups rather than separate dashboards.

### Key Lessons
- **GTFS-R Nuances:** Delays are best calculated per-stop (`TripUpdate`) rather than per-vehicle (`VehiclePosition`) for accuracy.
- **TimescaleDB Advantage:** Hypertables and continuous aggregates are essential for transit data volumes.

---

## Cross-Milestone Trends

### Execution Performance

| Milestone | Duration | Phases | Plans | Tasks | LOC Change |
|-----------|----------|--------|-------|-------|------------|
| v1.0 | 167 days | 3 | 9 | 40+ | +1,000 |

### Tech Debt Log

| Item | Origin | Impact | Status |
|------|--------|--------|--------|
| Mock Stop Data | Phase 1 | UI mismatch | Open (v1.1) |
| CSV Loading Speed | Phase 1 | Startup delay | Acceptable |
