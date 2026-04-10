# Phase 2: Historical Storage & Infrastructure - Research

## Context
Phase 2 focuses on moving from ephemeral MongoDB storage to structured, time-series optimized storage in TimescaleDB. This enables longitudinal analysis (REL-02) and prepares for statistical PDF generation in Phase 3.

## Stack Selection
- **Database:** `timescale/timescaledb:latest-pg17`. 
- **Driver:** `asyncpg` for raw performance or `SQLAlchemy` with `asyncpg` for better modeling. Given the batching requirement (D-03), `asyncpg` is preferred for its superior `copy_records_to_table` performance.
- **Python Libraries:** `asyncpg`, `pydantic`.

## Data Modeling
### Table: `delay_observations`
| Column | Type | Description |
|--------|------|-------------|
| `observed_at` | TIMESTAMPTZ | Time of observation (feed timestamp) |
| `stop_id` | TEXT | GTFS Stop ID |
| `route_id` | TEXT | GTFS Route ID |
| `trip_id` | TEXT | GTFS Trip ID |
| `delay_seconds` | INTEGER | Calculated deviation |

### Table: `active_vehicles` (Replacing MongoDB)
| Column | Type | Description |
|--------|------|-------------|
| `vehicle_id` | TEXT PRIMARY KEY | |
| `route_id` | TEXT | |
| `trip_id` | TEXT | |
| `latitude` | FLOAT | |
| `longitude` | FLOAT | |
| `updated_at` | TIMESTAMPTZ | |

## Implementation Patterns
### TimescaleDB Setup
- Create hypertable on `delay_observations` using `observed_at`.
- Enable compression for data older than 7 days.
- Create continuous aggregates for hourly delay stats (mean, stddev, p95).

### Batch Processing (D-03)
- Use a `list` to buffer observations in `delay_consumer.py`.
- Trigger flush based on `len(buffer) >= 100` or `time.time() - last_flush >= 10`.
- Use `asyncpg.Connection.copy_records_to_table` for high-speed batch insertion.

## Potential Pitfalls
- **Memory Leak:** Ensure buffer is cleared correctly after successful flush.
- **Async Safety:** Ensure the consumer loop doesn't block while waiting for DB flushes.
- **Migration Timing:** Need a plan to swap `api.py` and `frontend` from Mongo to SQL to prevent downtime (though v1 is demo-stage).

## Validation Architecture
- **Automated Tests:** Python script to verify batch inserts and hypertable creation.
- **Schema Validation:** Ensure SQL schema matches expected Pydantic models in `api.py`.
- **Query Performance:** Test time-bucketed queries against a synthetic dataset of 1M rows.
