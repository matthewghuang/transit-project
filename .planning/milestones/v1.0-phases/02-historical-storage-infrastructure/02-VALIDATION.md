# Phase 2: Historical Storage & Infrastructure - Validation Strategy

**Date:** April 09, 2026
**Phase:** 02

## Goal
Verify that delay observations are reliably persisted to TimescaleDB and that the system can handle continuous high-velocity writes.

## Dimension 8: Verification Architecture

### Automated Verification
- **V-01 (Connectivity):** Script to verify `postgres` container is reachable and TimescaleDB extension is active.
- **V-02 (Schema):** Verify `delay_observations` is a hypertable and `active_vehicles` table exists.
- **V-03 (Batch Integrity):** Insert 1000 records via `delay_consumer.py` logic and verify 1000 records exist in DB.
- **V-04 (Aggregation):** Verify continuous aggregate view returns valid stats for a known dataset.

### Performance Verification
- **P-01 (Throughput):** Measure latency of batch flush vs individual inserts.
- **P-02 (Storage):** Verify TimescaleDB compression reduces storage footprint for historical data.

### Integration Verification
- **I-01 (API):** `api.py` returns 200 for vehicle lookups using SQL instead of MongoDB.
- **I-02 (Consumer):** `delay_consumer.py` runs for 10 minutes without unhandled exceptions or memory growth.
