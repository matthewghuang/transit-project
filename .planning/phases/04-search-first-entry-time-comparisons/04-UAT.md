---
status: diagnosed
phase: 04-search-first-entry-time-comparisons
source: 04-01-SUMMARY.md, 04-02-SUMMARY.md, 04-03-SUMMARY.md, 04-04-SUMMARY.md
started: 2026-04-10T18:15:00Z
updated: 2026-04-10T19:30:00Z
---

## Current Test
[testing complete]

## Tests

### 1. Search for a Bus Stop by Route (R5)
expected: Typing a bus route name like "R5" into the search box shows stops that serve that specific route.
result: pass

### 2. Search for a Bus Stop by ID (50959)
expected: Entering "50959" prioritizes "Westbound E Hastings St @ Renfrew St" at the top of the results list.
result: issue
reported: "It does not show that stop. It doesn't show any stops. For some reason that stop is labellled as #959 not #50959"
severity: major

### 3. Hero Time UI Refinement
expected: The Time Triad no longer shows the "green circle prediction" indicator. The Stop Dashboard no longer contains the "About this stop" card. Hero time labels are clear and non-redundant.
result: issue
reported: "The time triad is not centered on the page. It shouldn't show prediction under the time."
severity: minor

### 4. PDF Chart Visibility
expected: Expanding the Time Triad reveals the historical delay distribution chart (PDF) with visible data points.
result: issue
reported: "It shows, but now actual time is missing"
severity: major

### 5. Search for a Bus Stop by Name (Regression)
expected: Typing "Main & 41st" still provides relevant suggestions.
result: pass

### 6. Stop Dashboard Transition (Regression)
expected: Selecting a stop smoothly transitions to the dashboard view.
result: pass

## Summary

total: 6
passed: 3
issues: 3
pending: 0
skipped: 0

## Gaps

- truth: "Entering a 5-digit stop ID (e.g., 50959) returns the correct stop."
  status: failed
  reason: "User reported: It does not show that stop. It doesn't show any stops. For some reason that stop is labellled as #959 not #50959"
  severity: major
  test: 2
  root_cause: "The stop_id '50959' is being stored or interpreted as '959', likely due to integer casting in the ingest or search logic removing leading zeros (though 50959 has none) or a data truncation issue."
  artifacts:
    - path: "api.py"
      issue: "search_stops logic might be truncating or incorrectly formatting stop IDs"
  missing:
    - "Verify stop_id storage format in PostgreSQL and ensuring string-based ID comparison in the search query."
  debug_session: ".planning/debug/uat-gap-stop-id-prefix.md"

- truth: "Time Triad is visually polished and centered."
  status: failed
  reason: "User reported: The time triad is not centered on the page. It shouldn't show prediction under the time."
  severity: minor
  test: 3
  root_cause: "CSS centering missing for the stop-dashboard main section and residual UI labels in TimeTriad.tsx."
  artifacts:
    - path: "frontend/src/App.css"
      issue: "Dashboard layout not centered"
    - path: "frontend/src/components/TimeTriad.tsx"
      issue: "Redundant prediction label under hero time"
  missing:
    - "Center dashboard layout and remove prediction subtitle."
  debug_session: ".planning/debug/uat-gap-ui-polishing.md"

- truth: "Expanded view shows all relevant times and the PDF chart."
  status: failed
  reason: "User reported: It shows, but now actual time is missing"
  severity: major
  test: 4
  root_cause: "Task 3 in Plan 04-04 may have introduced a regression or conditional rendering issue where 'actual_time' is hidden when the chart is visible."
  artifacts:
    - path: "frontend/src/components/TimeTriad.tsx"
      issue: "Actual time missing in expanded view"
  missing:
    - "Ensure all triad times remain visible when expanded."
  debug_session: ".planning/debug/uat-gap-actual-time-missing.md"
