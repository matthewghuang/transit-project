---
phase: quick
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: ["api.py", "frontend/src/hooks/useNextBuses.ts", "frontend/src/components/Map.tsx"]
autonomous: true
requirements: ["QUICK-01"]
must_haves:
  truths:
    - "User can see the scheduled time of the next bus for a selected stop"
    - "User can see the actual time of the next bus including real-time delays"
    - "User can see the predicted time of the next bus based on historical delay distributions"
  artifacts:
    - path: "api.py"
      provides: "New endpoint /api/stops/{stop_id}/next_buses"
    - path: "frontend/src/hooks/useNextBuses.ts"
      provides: "Hook for fetching next buses"
    - path: "frontend/src/components/Map.tsx"
      provides: "UI rendering of the three required bus times in the stop popup"
  key_links:
    - from: "frontend/src/components/Map.tsx"
      to: "/api/stops/{stop_id}/next_buses"
      via: "useNextBuses hook"
      pattern: "fetch.*api/stops"
---

<objective>
Enhance the stop click popup to display three new pieces of information: the scheduled time of the next bus, the actual time of the next bus (including current real-time delays), and a predicted time based on historical delay patterns.
Purpose: Give users actionable insights into when their bus will actually arrive, beyond simple distributions.
Output: An updated API serving next bus predictions and an enhanced UI displaying these times.
</objective>

<context>
@.planning/STATE.md
@api.py
@frontend/src/components/Map.tsx
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add Next Buses API Endpoint</name>
  <files>api.py</files>
  <action>Create a new GET endpoint `/api/stops/{stop_id}/next_buses`. This endpoint should determine the next scheduled bus for the stop (by parsing `google_transit/stop_times.txt` or a loaded memory cache), fetch its current real-time delay (from `active_vehicles` or realtime state), and calculate a historical prediction based on median delay for that time of day from `delay_observations` (reusing logic from `/api/distribution/{stop_id}`). Return an object containing `scheduled_time`, `actual_time`, and `predicted_time`.</action>
  <verify>
    <automated>curl -s http://localhost:8000/api/stops/10001/next_buses | grep predicted_time</automated>
  </verify>
  <done>Endpoint returns JSON with the three calculated times for a given stop.</done>
</task>

<task type="auto">
  <name>Task 2: Create React Hook and Update UI</name>
  <files>frontend/src/hooks/useNextBuses.ts, frontend/src/components/Map.tsx</files>
  <action>Create `useNextBuses(stopId: string | null)` to fetch data from the new endpoint. In `Map.tsx`, when a stop is clicked and `selectedStopId` is active, fetch the next bus times using the hook. Render the scheduled time, actual time (with delay), and predicted time (based on history) cleanly inside the existing `<Popup>` for the stop, just above or below the DelayDistributionChart.</action>
  <verify>
    <automated>npm run lint -- --ext .ts,.tsx frontend/src/components/Map.tsx</automated>
  </verify>
  <done>The React components compile without errors, use the new hook, and render the three requested times in the UI popup.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Client -> API | Frontend fetching next bus data from API |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-quick-01 | Spoofing | /api/stops/{stop_id}/next_buses | accept | No authentication required for public transit data. |
| T-quick-02 | Denial of Service | /api/stops/{stop_id}/next_buses | mitigate | Validate stop_id parameter size and sanitize input to prevent slow queries or memory exhaustion. |
</threat_model>

<verification>
Ensure the API handles cases where no next bus is scheduled for the day gracefully (returning nulls or an empty state), and that the UI renders a sensible fallback (e.g., "No upcoming buses scheduled").
</verification>

<success_criteria>
Clicking a stop on the map displays the scheduled time, actual time, and historically predicted time of the next bus.
</success_criteria>

<output>
After completion, create `.planning/quick/260409-uhf-when-a-user-clicks-a-stop-it-should-show/quick-01-SUMMARY.md`
</output>