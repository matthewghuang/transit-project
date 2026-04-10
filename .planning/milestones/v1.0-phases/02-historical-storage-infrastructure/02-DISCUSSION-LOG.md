# Phase 2: Historical Storage & Infrastructure - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-09
**Phase:** 02-historical-storage-infrastructure
**Areas discussed:** Database Setup, Persistence Pattern, Aggregation & Retention, Migration

---

## Database Setup

| Option | Description | Selected |
|--------|-------------|----------|
| TimescaleDB via Docker | Containerized time-series database. | ✓ |
| External Managed Postgres | Cloud-hosted instance. | |
| Standard Postgres | Vanilla PG without hypertables. | |

**User's choice:** TimescaleDB via Docker
**Notes:** User chose Docker for infrastructure consistency.

---

## Persistence Pattern

| Option | Description | Selected |
|--------|-------------|----------|
| Batch Inserts | Accumulate and flush records in groups. | ✓ |
| Sync Write-through | Write immediately on each record. | |
| Async Background | Hand off writes to separate task. | |

**User's choice:** Batch Inserts
**Notes:** Chosen for performance efficiency.

---

## Aggregation & Retention

| Option | Description | Selected |
|--------|-------------|----------|
| Continuous Aggregates | Auto-pre-calculate summaries via Timescale. | ✓ |
| Raw Only | Keep all discrete points indefinitely. | |
| Summary Tables | Manual cron-based aggregation. | |

**User's choice:** Continuous Aggregates
**Notes:** Leverages TimescaleDB native features.

---

## Migration

| Option | Description | Selected |
|--------|-------------|----------|
| Migrate to SQL | Replace MongoDB entirely. | ✓ |
| Dual Storage | Keep Mongo for real-time, Postgres for historical. | |

**User's choice:** Migrate to SQL
**Notes:** User explicitly requested consolidating to SQL.

---

## the agent's Discretion

- Exact SQL schema and batch parameters.

## Deferred Ideas

- API statistical engine (Phase 3).
- Visualization dashboard (Phase 3).
