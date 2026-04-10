---
status: passed
phase: 03-probabilistic-api-visualization
source: [03-01-SUMMARY.md, 03-02-SUMMARY.md, 03-03-SUMMARY.md]
started: 2026-04-10T03:50:00Z
updated: 2026-04-10T04:20:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

[testing complete]

## Tests

### 1. Cold Start Smoke Test
expected: Kill any running server/service. Clear ephemeral state (temp DBs, caches, lock files). Start the application from scratch. Server boots without errors, any seed/migration completes, and a primary query (health check, homepage load, or basic API call) returns live data.
result: pass

### 2. Probabilistic Distribution API
expected: Fetch data from `/api/distribution/{stop_id}` (use a known stop ID from the map). The response should contain a 'median' delay and a 'buckets' array of 1-minute intervals representing the delay distribution.
result: pass

### 3. Delay Distribution Area Chart
expected: Click on a stop marker on the Leaflet map. A popup should appear, lazily load the distribution chart, and display a shaded area curve showing the historical lateness likelihood for that stop.
result: pass

### 4. Median Delay Badge
expected: Within the stop popup distribution chart, a prominent summary badge or text should state the typical delay (e.g., "Usually arrives +2m late"), matching the median value returned by the API.
result: pass

## Summary

total: 4
passed: 4
issues: 0
pending: 0
skipped: 0

## Gaps

All gaps resolved by integrating `db-init` service into `docker-compose.yml` and enhancing `db_init.py` with retry logic.

