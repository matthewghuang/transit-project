---
status: diagnosed
updated: 2026-04-10T19:00:00Z
---

## Current Focus

hypothesis: The API endpoint `/api/stops/{stop_id}/next_buses` is being called with a `stop_code` (e.g., 50959) instead of a `stop_id` (e.g., 968), causing the `stop_times_lookup` to return no results.
test: Verify what ID the frontend sends and how the backend handles `stop_code` vs `stop_id`.
expecting: Confirmed that passing `50959` to the API returns empty results because the internal lookup expects `968`.
next_action: None (find_root_cause_only)

## Symptoms


expected: The dashboard should display the scheduled time plus the delay provided by the GTFS Realtime API.
actual: It shows "--:--:--" for all stops.
errors: No specific errors reported, but the field fails to populate.
reproduction: Search for stop #50959 or #959 and view the next bus arrival card.
started: Phase 4 UI and API changes.

## Eliminated

## Evidence

- timestamp: 2026-04-10T18:30:00Z
  checked: `frontend/src/components/TimeTriad.tsx`
  found: The UI displays `--:--:--` when `actual_time` is null.
  implication: The issue is that the backend returns `null` for `actual_time`.

- timestamp: 2026-04-10T18:35:00Z
  checked: `api.py` endpoint `/api/stops/{stop_id}/next_buses`
  found: The backend attempts to fetch `delay_seconds` from `trip_delays` table using `trip_id` from `stop_times_lookup`.
  implication: If `trip_delays` is empty or doesn't match the `trip_id`, `actual_time` remains null.

- timestamp: 2026-04-10T18:40:00Z
  checked: `delay_consumer.py`
  found: It consumes from `trip_updates` topic and updates `trip_delays` and `delay_observations` tables.
  implication: The data pipeline seems correct, but there might be a mismatch in IDs or the consumer isn't running/receiving data.

- timestamp: 2026-04-10T18:45:00Z
  checked: `google_transit/stops.txt` and `stop_times.txt`
  found: For stop #50959, the `stop_code` is `50959` but the `stop_id` is `968`. The API uses `stop_id` for lookups.
  implication: If the user searches by `50959` (stop_code), the frontend might be passing `50959` to `/api/stops/50959/next_buses`. But `stop_times_lookup` is indexed by `stop_id` (`968`).

- timestamp: 2026-04-10T18:50:00Z
  checked: `api.py` `load_stop_times()`
  found: `stop_times_lookup` uses `row["stop_id"]` as key.
  implication: Lookup will fail if `stop_code` is passed as `stop_id`.

## Resolution

root_cause: The API endpoint `/api/stops/{stop_id}/next_buses` expects a GTFS `stop_id`, but the frontend (and users) often use the `stop_code` (e.g., 50959). In the Translink dataset, `stop_id` and `stop_code` are often different (e.g., `stop_id=968` for `stop_code=50959`). When the API is called with a `stop_code` that doesn't exist as a `stop_id`, `stop_times_lookup.get(stop_id)` returns `None`, leading to a default response with all times as `null`, which the frontend renders as "--:--:--".
fix: 
verification: 
files_changed: []
