---
status: diagnosed
trigger: "Investigate issue: actual-time-missing-triad"
created: 2026-04-10T00:00:00Z
updated: 2026-04-10T16:45:00Z
---

## Current Focus

hypothesis: The actual time is missing because the backend query for `current_delay` in `api.py` filters by `trip_id` but not `stop_id`, and `delay_observations` only contains data for the *first* stop of a trip update, which rarely matches the specific stop being queried.
test: Confirmed via code analysis of `api.py` and `delay_consumer.py`.
expecting: Root cause identified.
next_action: Return diagnosis.

## Symptoms

expected: The actual (real-time) arrival time should be visible in the expanded triad grid.
actual: It shows "--:--:--" for every stop.
errors: None reported by user, but UI displays placeholder.
reproduction: Search for any stop and expand the Time Triad card.
started: Started recently, likely after Phase 04 Plan 06 UI polishing.

## Eliminated

## Evidence

- timestamp: 2026-04-10T16:30:00Z
  checked: `api.py` line 496
  found: The query `SELECT delay_seconds FROM delay_observations WHERE trip_id = $1 ORDER BY observed_at DESC LIMIT 1` retrieves the latest delay for a trip across ALL stops.
  implication: This might provide a delay, but it doesn't guarantee the delay is relevant for the *current* stop. However, it should at least return *something* if any stop on that trip has an observation.
- timestamp: 2026-04-10T16:35:00Z
  checked: `delay_consumer.py` line 170-206
  found: The consumer only records the delay for the *first* stop in the `stop_time_update` list (`sorted_updates[0]`).
  implication: Most stops will NEVER have a record in `delay_observations` for a specific `trip_id` unless they happen to be the first stop in a specific GTFS-R update. Since `api.py` queries by `trip_id`, if the trip hasn't reached that stop yet or the consumer hasn't seen an update for that specific stop, `current_delay` will be null.
- timestamp: 2026-04-10T16:40:00Z
  checked: `api.py` lines 471-474
  found: The schedule lookup `arr_sec >= now_sec` finds the *future* scheduled arrival.
  implication: If the consumer only records delays for stops as they are "current" (the first update in the list), there is a high probability that a future stop has no `delay_observations` record yet, or the last record for that `trip_id` is for a different stop.

## Resolution

root_cause: The `delay_observations` table only stores a single observation (the first one) per GTFS-R trip update. The API in `api.py` attempts to fetch the latest delay for a `trip_id` to calculate `actual_time`, but because observations are sparse and typically represent the bus's current position, future stops (which the user is searching for) often have no relevant or recent delay data in that table. Additionally, filtering only by `trip_id` without `stop_id` makes the data unreliable for specific stop arrival times.
fix: 
verification: 
files_changed: []
