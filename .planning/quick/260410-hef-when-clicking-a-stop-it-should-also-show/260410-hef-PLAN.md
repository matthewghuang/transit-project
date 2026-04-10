---
phase: quick
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [frontend/src/components/StopDashboard.tsx]
autonomous: true
requirements: [STOP-NAME-UI]
must_haves:
  truths:
    - "Stop name is displayed in the StopDashboard header next to or instead of the Stop ID"
  artifacts:
    - path: "frontend/src/components/StopDashboard.tsx"
      provides: "Stop name display"
---

<objective>
Display the stop name in the StopDashboard header when a stop is selected.

Purpose: Improve UX by providing semantic context (stop name) rather than just a numerical ID.
Output: Modified StopDashboard.tsx that fetches/finds and displays the stop name.
</objective>

<execution_context>
@/Users/turq/code/transit-data/.opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@frontend/src/components/StopDashboard.tsx
@frontend/src/hooks/useStops.ts
@frontend/src/api/database.ts
</context>

<tasks>

<task type="auto">
  <name>Task 1: Update StopDashboard to display stop name</name>
  <files>frontend/src/components/StopDashboard.tsx</files>
  <action>
    Modify `StopDashboard.tsx` to:
    1. Import and use the `useStops` hook to get the list of available stops.
    2. Find the stop object that matches the `stopId` prop.
    3. Update the `<h2>` tag in the header to display the stop's name (e.g., "{stop.name} (#{stopId})") instead of just "Stop #{stopId}".
    4. Handle the loading/missing state gracefully (e.g., fall back to "Stop #{stopId}" if the name isn't found yet).
  </action>
  <verify>
    <automated>grep -q "useStops" frontend/src/components/StopDashboard.tsx</automated>
  </verify>
  <done>Stop name is visible in the header when StopDashboard is rendered.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries
| Boundary | Description |
|----------|-------------|
| API -> Frontend | Stop data from /api/stops is rendered in the UI |

## STRIDE Threat Register
| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-quick-01 | XSS | StopDashboard.tsx | mitigate | React handles basic escaping by default for text content in h2 |
</threat_model>

<verification>
Check that selecting a stop in the UI now shows the Stop Name in the header.
</verification>

<success_criteria>
The header shows the human-readable stop name.
</success_criteria>

<output>
After completion, create .planning/quick/260410-hef-when-clicking-a-stop-it-should-also-show/01-01-SUMMARY.md
</output>
