---
phase: 260410-klm
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [frontend/src/App.css]
autonomous: false
requirements: [FIX-UI-01]
must_haves:
  truths:
    - "Stop name in dashboard header does not overflow on mobile screens"
    - "Stop name is truncated with ellipsis if it exceeds available width"
  artifacts:
    - path: "frontend/src/App.css"
      provides: "CSS rules for dashboard header text overflow"
---

<objective>
Fix the header text overflow on mobile for the StopDashboard component. When a stop name is long, it currently overflows the header container. This plan will add CSS rules to ensure the text is truncated with an ellipsis and does not break the layout.
</objective>

<execution_context>
@/Users/turq/code/transit-data/.opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@frontend/src/components/StopDashboard.tsx
@frontend/src/App.css
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add overflow handling to dashboard header</name>
  <files>frontend/src/App.css</files>
  <action>
    Add CSS rules to `frontend/src/App.css` to handle text overflow in the `.stop-title` and its contained `h2`.
    
    The rules should:
    1. Ensure `.stop-title` has `flex: 1` and `min-width: 0` (standard flexbox fix for truncation).
    2. Add `white-space: nowrap`, `overflow: hidden`, and `text-overflow: ellipsis` to the `h2` within `.stop-title`.
  </action>
  <verify>
    <automated>grep -A 10 ".stop-title" frontend/src/App.css | grep "text-overflow: ellipsis"</automated>
  </verify>
  <done>CSS rules for truncation are present in App.css</done>
</task>

<task type="checkpoint:human-verify">
  <name>Task 2: Verify header layout on mobile device</name>
  <action>
    Manually verify the fix in the browser using mobile emulation.
  </action>
  <what-built>Mobile-responsive dashboard header with text truncation</what-built>
  <how-to-verify>
    1. Start the frontend dev server: `cd frontend && npm run dev`
    2. Open the app in a browser (usually http://localhost:1234 or similar).
    3. Search for a stop with a long name (e.g., "Marine Dr Station @ Bay 1").
    4. Open the browser's developer tools and toggle device toolbar (mobile view).
    5. Verify the stop name in the header is truncated with "..." instead of overflowing or pushing the back button out of view.
  </how-to-verify>
  <verify>
    <automated>true</automated>
  </verify>
  <done>Visual verification complete</done>
  <resume-signal>approved</resume-signal>
</task>

</tasks>

<threat_model>
## Trust Boundaries
N/A - UI/CSS only change.

## STRIDE Threat Register
| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-01-01 | N/A | UI Layout | accept | Low risk, cosmetic fix only. |
</threat_model>

<verification>
Ensure the header remains functional and the back button is accessible on small screens.
</verification>

<success_criteria>
Stop names in the dashboard header are gracefully truncated with an ellipsis on mobile devices, maintaining the layout integrity.
</success_criteria>

<output>
After completion, create .planning/phases/260410-klm-on-mobile-the-header-text-that-displays-/260410-klm-01-SUMMARY.md
</output>
