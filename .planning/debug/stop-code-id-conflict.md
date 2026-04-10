---
status: diagnosed
trigger: "Investigate issue: stop-code-id-conflict"
created: 2026-04-10T10:00:00Z
updated: 2026-04-10T10:00:00Z
---

## Current Focus

hypothesis: The backend or frontend is incorrectly mapping or preferring the internal `stop_id` over the user-visible `stop_code` in the dashboard header and lookup logic.
test: Trace the stop data from the search action to the dashboard display, checking where the ID is switched.
expecting: To find a point where `stop_code` is replaced by `stop_id` or where `stop_id` is used for display.
next_action: "ROOT CAUSE FOUND"

## Symptoms

expected: The application should use the stop code (e.g., 50959) as the unique identifier in both the frontend and backend.
actual: The dashboard header shows the internal ID "968" instead of the code "50959".
errors: ID confusion causing display and likely lookup issues.
reproduction: Search for stop #50959 and observe the dashboard header.
started: Since Phase 4 UI overhaul, persists after mapping fix.

## Eliminated

## Evidence

## Resolution

root_cause: The backend API and frontend search results prioritize the internal `stop_id` (e.g., "968") over the user-visible `stop_code` (e.g., "50959"). Specifically, `api.py` returns `stop_id` in the `id` field for search results and stop listings, which the frontend then uses for all subsequent display and API calls. While the backend has a resolution layer to accept `stop_code`, it immediately "resolves" it to `stop_id` and returns that internal ID back to the client.
fix: 1. Modify `api.py` to store and return `stop_code` as the primary identifier where available. 2. Implement an `id_to_stop_code` mapping in `api.py` to allow reverse lookup. 3. Update the `StopInfo` Pydantic model and endpoint logic to return the code as the `id`. 4. Ensure the dashboard display uses the `id` returned from the API, which will now be the stop code.
verification:
files_changed: []
