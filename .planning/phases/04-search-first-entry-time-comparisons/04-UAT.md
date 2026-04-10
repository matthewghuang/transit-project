---
status: diagnosed
phase: 04-search-first-entry-time-comparisons
source: 04-01-SUMMARY.md, 04-02-SUMMARY.md, 04-03-SUMMARY.md, 04-04-SUMMARY.md, 04-05-SUMMARY.md
started: 2026-04-10T18:15:00Z
updated: 2026-04-10T20:30:00Z
---

## Current Test
[testing complete]

## Tests

### 1. Search for a Bus Stop by ID (50959)
expected: Entering "50959" prioritizes "Westbound E Hastings St @ Renfrew St" at the top of the results list. The stop ID should be correctly displayed as #50959.
result: issue
reported: "Westbound E Hastings St @ Renfrew St displays as #959. Other stops have valid 5 digit IDs"
severity: major

### 2. Time Triad Centering & UI Cleanup
expected: The stop dashboard content (especially the Time Triad) is visually centered on the page. The "prediction" subtitle under the hero time is gone.
result: issue
reported: "it's not centered, prediction is still there"
severity: minor

### 3. Actual Time Visibility in Expanded View
expected: Expanding the Time Triad shows Scheduled, Actual, AND Predicted times clearly, even when the PDF chart is visible.
result: issue
reported: "yes but actual time is blank now"
severity: major

### 4. Search for a Bus Stop by Route (Regression)
expected: Typing "R5" still provides relevant stop suggestions.
result: pass

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

- truth: "Stop IDs are displayed correctly without truncation or prefix issues."
  status: resolved
  reason: "User reported: Westbound E Hastings St @ Renfrew St displays as #959. Other stops have valid 5 digit IDs"
  severity: major
  test: 1
  root_cause: "Residual integer casting or formatting in api.py for the '50959' case, combined with inconsistent display logic in HeroSearch.tsx."
  artifacts:
    - path: "api.py"
      issue: "search_stops logic still returning truncated IDs for certain numeric ranges"
    - path: "frontend/src/components/HeroSearch.tsx"
      issue: "Display logic for stop-id badge incorrectly formatting the ID string"
  missing:
    - "Strict string-based stop_id handling across the full stack."
  debug_session: ".planning/debug/uat-gap-stop-id-truncated.md"

- truth: "Time Triad is visually polished, centered, and subtitle removed."
  status: resolved
  reason: "User reported: it's not centered, prediction is still there"
  severity: minor
  test: 2
  root_cause: "CSS selector specificity in App.css prevents centering, and TimeTriad.tsx still contains the hardcoded status text block."
  artifacts:
    - path: "frontend/src/App.css"
      issue: "Insufficient layout constraints for dashboard centering"
    - path: "frontend/src/components/TimeTriad.tsx"
      issue: "Residual 'prediction' status text element"
  missing:
    - "Force center the triad container and delete the status text div."
  debug_session: ".planning/debug/uat-gap-ui-misalignment.md"

- truth: "Expanded view shows all relevant times and the PDF chart."
  status: resolved
  reason: "User reported: yes but actual time is blank now"
  severity: major
  test: 3
  root_cause: "Conditional logic in TimeTriad.tsx grid rendering was accidentally modified to hide the 'Actual' column when fixing PDF visibility."
  artifacts:
    - path: "frontend/src/components/TimeTriad.tsx"
      issue: "Broken conditional grid mapping for actual_time"
  missing:
    - "Restore actual_time mapping in the triad grid."
  debug_session: ".planning/debug/uat-gap-actual-time-blank.md"
