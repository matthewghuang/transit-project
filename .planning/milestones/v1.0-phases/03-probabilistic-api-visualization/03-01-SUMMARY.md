---
phase: 03-probabilistic-api-visualization
plan: 01
subsystem: backend
tags: [api, statistics, distributions]
key-files:
  created: [tests/test_api_distribution.py]
  modified: [api.py, pyproject.toml]
metrics:
  duration: 15m
  completed_date: "2026-04-10"
---

# Phase 03 Plan 01: Probabilistic API Summary

Implemented the `/api/distribution/{stop_id}` endpoint in FastAPI to provide probabilistic delay insights.

## Key Changes
- Added `numpy` dependency for statistical calculations.
- Implemented `/api/distribution/{stop_id}` endpoint.
  - Filters historical observations by a 2-hour time window centered on the current time.
  - Segregates data by DayType (Weekday vs Weekend).
  - Calculates median delay and 1-minute histogram buckets.
- Added Pydantic models for distribution responses.
- Created scaffold test suite for API verification.

## Known Stubs
None.

## Self-Check: PASSED
