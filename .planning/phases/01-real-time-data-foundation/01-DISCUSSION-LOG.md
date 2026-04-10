# Phase 1: Real-time Data Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-09
**Phase:** 01-real-time-data-foundation
**Areas discussed:** Integration Point, Static Data Ingestion, Delay Calculation, Frontend Presentation

---

## Integration Point

| Option | Description | Selected |
|--------|-------------|----------|
| New Parallel Consumer | Create a fresh `delay_consumer.py` that listens to Kafka. | ✓ |
| Extend `demo_consumer.py` | Add logic to existing consumer. | |

**User's choice:** New Parallel Consumer
**Notes:** User explicitly requested a parallel consumer to keep the pipeline clean.

---

## Static Data Ingestion

| Option | Description | Selected |
|--------|-------------|----------|
| In-Memory Dict | Load `{ (trip_id, stop_id): time }` into memory. | ✓ |
| SQL Lookup | Pre-load into Postgres and query on every message. | |
| Redis | Use external cache. | |

**User's choice:** In-Memory Dict
**Notes:** Chosen for performance and simplicity in Phase 1.

---

## Delay Calculation

| Option | Description | Selected |
|--------|-------------|----------|
| Strict Mode | Only use agency-provided `arrival.delay`. | ✓ |
| Calculated Mode | Guess delay based on coordinates + schedule. | |

**User's choice:** Strict Mode
**Notes:** Ensures data integrity for future probabilistic analysis.

---

## Frontend Presentation

| Option | Description | Selected |
|--------|-------------|----------|
| Map Popups | Click a stop to see incoming bus status. | ✓ |
| Sidebar Countdown | List of buses in a dedicated sidebar. | |
| Timeline View | Linear progress bar. | |

**User's choice:** Map Popups
**Notes:** Maintains map-centric UX for stop focus.

---

## the agent's Discretion

- Exact data structure for the schedule cache.
- Popup styling and UX nuance.

## Deferred Ideas

- Postgres/TimescaleDB storage (Phase 2).
- Statistical distribution charts (Phase 3).
