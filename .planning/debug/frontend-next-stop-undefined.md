---
status: awaiting_human_verify
trigger: "frontend bug: Uncaught TypeError: Cannot read properties of undefined (reading 'next_stop_id')"
created: 2026-04-09T00:00:00Z
updated: 2026-04-09T00:02:00Z
---

## Current Focus

hypothesis: CONFIRMED — Frontend types and property accesses assumed old MongoDB nested response shape but API returns flat TimescaleDB objects.
test: Build succeeds, no remaining references to old data shape.
expecting: Dashboard renders without TypeError crash.
next_action: Awaiting human verification that the dashboard loads in the browser.

## Symptoms

expected: Dashboard renders successfully without crashes
actual: TypeError crash when opening the map
errors: |
  Uncaught TypeError: Cannot read properties of undefined (reading 'next_stop_id')
      at Map.tsx:75:52
      at Array.filter
      at Map.tsx:75:26
      at Array.map
      at ef (Map.tsx:56:19)
reproduction: Opening the map page in the browser
started: After Phase 3 completion (area chart and distribution API integration)

## Eliminated

## Evidence

- timestamp: 2026-04-09T00:00:30Z
  checked: api.py VehicleUpdate Pydantic model
  found: API returns flat objects `{ id, trip: { tripId, routeId }, position: { latitude, longitude }, timestamp }`. No `vehicle` wrapper, no `next_stop_id`, no `delay_seconds`, no `route_name`.
  implication: Frontend's `PositionDocumentEntry.vehicle` will always be `undefined`.

- timestamp: 2026-04-09T00:00:40Z
  checked: frontend/src/api/database.ts types
  found: Frontend type `PositionDocumentEntry` expects `{ id, vehicle: Vehicle, timestamp, _id }` with nested Vehicle containing `trip`, `position`, `next_stop_id`, `delay_seconds`, etc. This is the old MongoDB response shape.
  implication: Every `pos.vehicle.*` access in the frontend will crash because `pos.vehicle` is `undefined`.

- timestamp: 2026-04-09T00:00:50Z
  checked: Map.tsx lines 30, 75, 78, 80, 83, 104-137 and FilterTable.tsx line 43
  found: All property accesses use `pos.vehicle.*` pattern — there are 12+ access sites that will crash. Line 75 crashes first because it runs inside MOCK_STOPS.map which executes on render.
  implication: Root cause is schema mismatch. Fix must update ALL access sites, not just line 75.

- timestamp: 2026-04-09T00:01:30Z
  checked: grep for all remaining old-shape references (.vehicle., ._id, next_stop_id, delay_seconds, route_name)
  found: Zero remaining references to old data shape in frontend source.
  implication: Fix is complete and comprehensive.

- timestamp: 2026-04-09T00:01:45Z
  checked: Frontend build (npm run build)
  found: Build succeeds cleanly — "Built in 1.59s" with no errors.
  implication: TypeScript compilation passes, all property accesses are valid.

## Resolution

root_cause: Frontend types (database.ts) and property access patterns (Map.tsx, FilterTable.tsx) assumed the old MongoDB nested response shape with a `vehicle` wrapper object. The API was refactored to TimescaleDB and returns flat VehicleUpdate objects `{ id, trip, position, timestamp }`. Every `pos.vehicle.*` access fails because `pos.vehicle` is `undefined`. The crash at line 75 (`pos.vehicle.next_stop_id`) is the first to execute during render because it's inside the MOCK_STOPS.map() which runs unconditionally.
fix: (1) Rewrote database.ts types to match actual API response shape — replaced PositionDocumentEntry/Vehicle/VehicleInfo with flat VehicleUpdate type. (2) Updated all property accesses in Map.tsx from `pos.vehicle.*` to `pos.*` (12+ sites). (3) Replaced next_stop_id arrival-matching section with placeholder since API doesn't provide that field. (4) Updated FilterTable.tsx to use `pde.trip.routeId` instead of `pde.vehicle.trip.route_name`.
verification: Build succeeds cleanly. Zero remaining references to old data shape. Awaiting human browser verification.
files_changed: [frontend/src/api/database.ts, frontend/src/components/Map.tsx, frontend/src/components/FilterTable.tsx]
