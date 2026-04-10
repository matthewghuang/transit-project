---
status: diagnosed
phase: 04-search-first-entry-time-comparisons
source: 04-01-SUMMARY.md, 04-02-SUMMARY.md, 04-03-SUMMARY.md
started: 2026-04-10T18:15:00Z
updated: 2026-04-10T18:55:00Z
---

## Current Test
[testing complete]

## Tests

### 1. Search for a Bus Stop by Name
expected: Typing an intersection (e.g., "Main & 41st") into the search box shows an auto-suggest dropdown with relevant transit stops. Results are filtered and ranked as you type (fuzzy matching).
result: issue
reported: "It works but when I search for a bus like \"R5\" it should show stops that have the R5."
severity: major

### 2. Search for a Bus Stop by ID
expected: Entering a 5-digit stop number (e.g., "50001") prioritizes that specific stop in the results list, and clicking it takes you directly to the dashboard.
result: issue
reported: "50959 should return \"Westbound E Hastings St @ Renfrew St\" but it does not"
severity: major

### 3. Stop Dashboard & Hero Time
expected: Selecting a stop opens the Stop Dashboard. A single large "Hero Time" is displayed, which is the earliest of the Scheduled, Actual (real-time), or Predicted (historical) times. The time source is clearly labeled.
result: issue
reported: "I don't like the green circle with \"prediction\" that seems useless. The card with \"About this stop\" seems useless as well. And the scheduled time is the same as actual time (this is weird)"
severity: major

### 4. Time Triad Expansion
expected: Clicking the Hero Time expands the view to show all three times (Scheduled, Actual, Predicted) side-by-side, along with the historical delay distribution chart.
result: issue
reported: "It does not show the PDF."
severity: major

### 5. Recent Search History
expected: After searching and selecting a stop, returning to the landing page shows that stop in a \"Recent Searches\" section for quick re-access.
result: pass

### 6. Map Removal Verification
expected: The landing page no longer shows a map. There are no Leaflet-related errors in the console, and the page loads faster due to the removed dependencies.
result: pass

## Summary

total: 6
passed: 2
issues: 4
pending: 0
skipped: 0

## Gaps

- truth: "Typing a bus route name into the search box shows stops that serve that route."
  status: failed
  reason: "User reported: It works but when I search for a bus like \"R5\" it should show stops that have the R5."
  severity: major
  test: 1
  root_cause: "The SQL search query in api.py only filters by stop_id or stop_name and does not join with the routes/trips tables to filter by route_short_name."
  artifacts:
    - path: "api.py"
      issue: "search_stops function missing route-based filtering logic"
  missing:
    - "Add JOIN with delay_observations or stops_routes mapping table to enable searching by route name."
  debug_session: ".planning/debug/uat-gap-route-search.md"

- truth: "Entering a 5-digit stop ID returns the correct stop."
  status: failed
  reason: "User reported: 50959 should return \"Westbound E Hastings St @ Renfrew St\" but it does not"
  severity: major
  test: 2
  root_cause: "The numeric check 'is_numeric = q.isdigit() and (len(q) >= 4 and len(q) <= 6)' is correct, but the SQL query prioritizes similarity(stop_name, q) which may drown out exact ID matches if many names contain the digits."
  artifacts:
    - path: "api.py"
      issue: "SQL query in search_stops doesn't sufficiently prioritize exact stop_id matches."
  missing:
    - "Strengthen ORDER BY weight for exact stop_id matches."
  debug_session: ".planning/debug/uat-gap-stop-id-search.md"

- truth: "Hero Time is distinct from scheduled/actual and clearly labeled with valuable context."
  status: failed
  reason: "User reported: I don't like the green circle with \"prediction\" that seems useless. The card with \"About this stop\" seems useless as well. And the scheduled time is the same as actual time (this is weird)"
  severity: major
  test: 3
  root_cause: "1. TimeTriad.tsx renders a 'prediction' indicator that the user finds cluttered. 2. StopDashboard.tsx includes a hardcoded 'About this stop' card. 3. useNextBuses.ts/api.py fallback logic causes duplication of scheduled/actual times."
  artifacts:
    - path: "frontend/src/components/TimeTriad.tsx"
      issue: "Cluttered UI indicators ('green circle')"
    - path: "frontend/src/components/StopDashboard.tsx"
      issue: "Redundant informational cards"
    - path: "api.py"
      issue: "Fallback logic in get_next_buses causes identical times when data is missing"
  missing:
    - "Clean up TimeTriad.tsx UI."
    - "Remove info card from StopDashboard.tsx."
    - "Ensure actual/predicted times are null if unavailable, rather than duplicating scheduled time."
  debug_session: ".planning/debug/uat-gap-ui-clutter.md"

- truth: "Expanded view shows Scheduled, Actual, Predicted times and historical PDF."
  status: failed
  reason: "User reported: It does not show the PDF."
  severity: major
  test: 4
  root_cause: "DelayDistributionChart.tsx is imported but either not rendering data or the API returns empty buckets for the selected stop/time window."
  artifacts:
    - path: "frontend/src/components/TimeTriad.tsx"
      issue: "DelayDistributionChart not visible or data-starved"
  missing:
    - "Verify PDF data flow and chart rendering conditions."
  debug_session: ".planning/debug/uat-gap-pdf-missing.md"
