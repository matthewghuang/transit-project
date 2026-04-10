---
phase: 01-real-time-data-foundation
reviewed: 2026-04-09T14:30:00Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - api.py
  - delay_consumer.py
  - frontend/src/api/database.ts
  - frontend/src/components/Map.tsx
  - main.py
findings:
  critical: 0
  warning: 2
  info: 3
  total: 5
status: issues_found
---

# Phase 01: Real-time Data Foundation Review Report

**Reviewed:** 2026-04-09T14:30:00Z
**Depth:** standard
**Files Reviewed:** 5
**Status:** issues_found

## Summary

The foundation for real-time data ingestion and delay processing is well-structured. The system successfully polls both vehicle positions and trip updates, calculates delays by cross-referencing GTFS static schedules, and surfaces this information through the API to the frontend.

Key areas for improvement include handling midnight transitions in delay calculations and adding robustness to the Kafka producer.

## Warnings

### WR-01: Midnight Transition in Delay Calculation

**File:** `delay_consumer.py:133-145`
**Issue:** The delay calculation uses `get_seconds_since_start_of_day`, which does not account for trips crossing midnight or "GTFS days" that extend beyond 24 hours (e.g., a 25:00:00 arrival time). If a bus is scheduled at 23:55 and arrives at 00:05, the current logic will calculate a massive negative delay.
**Fix:**
```python
# Use absolute timestamps for comparison where possible, 
# or normalize both scheduled and actual times relative to the trip start date.
def calculate_delay(actual_ts, scheduled_seconds, trip_start_date):
    # Convert trip_start_date and scheduled_seconds to a UTC timestamp
    # Then compare with actual_ts
    pass
```

### WR-02: Synchronous Kafka Production in Polling Loop

**File:** `main.py:65-72`
**Issue:** `producer.produce` is called synchronously within the polling loop. While `produce` is technically asynchronous in `confluent-kafka`, the script then calls `producer.flush()` (line 87) which blocks the entire polling loop until all messages are delivered. If Kafka is slow or unreachable, it will delay subsequent polling cycles.
**Fix:** Consider using a delivery callback to log errors asynchronously and remove the `flush()` call from the main loop, or move it to a background thread.

## Info

### IN-01: Hardcoded Timezone Assumption

**File:** `delay_consumer.py:65`
**Issue:** The code assumes the system time or the Translink timestamp matches the "Pacific Time" context of the GTFS data.
**Fix:** Use `pytz` or `zoneinfo` to explicitly handle `America/Vancouver` time when converting timestamps to "seconds since start of day".

### IN-02: Missing Schema Validation for GTFS-R

**File:** `main.py:44`
**Issue:** `feed.ParseFromString(response.content)` is called without checking if the content is actually a valid GTFS-R message beyond basic Protobuf parsing.
**Fix:** Add validation to ensure `feed.header.gtfs_realtime_version` is present.

### IN-03: Frontend Type Safety

**File:** `frontend/src/api/database.ts:30`
**Issue:** `delay_seconds` is optional in the TypeScript type, which is correct, but the Map component doesn't handle the case where `delay_seconds` might be a very large outlier due to calculation errors.
**Fix:** Add a bounds check in `Map.tsx` before rendering the delay string (e.g., `if (Math.abs(delay) < 3600)`).

---

_Reviewed: 2026-04-09T14:30:00Z_
_Reviewer: antigravity (gsd-code-reviewer)_
_Depth: standard_
