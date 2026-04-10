---
phase: 05-cleanup
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [frontend/src/App.tsx, frontend/src/App.css]
autonomous: true
requirements: [UI-01]
must_haves:
  truths:
    - "The main application header 'Transit Dashboard' is removed"
    - "The white sidebar (secondary grid column) is removed from the layout"
  artifacts:
    - path: "frontend/src/App.tsx"
      provides: "Simplified main app structure"
    - path: "frontend/src/App.css"
      provides: "Updated grid layout without sidebar"
  key_links: []
---

<objective>
Remove the 'Transit Dashboard' header and the white sidebar from the hero/main layout to create a cleaner, more focused UI.
</objective>

<execution_context>
@/Users/turq/code/transit-data/.opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@frontend/src/App.tsx
@frontend/src/App.css
</context>

<tasks>

<task type="auto">
  <name>Task 1: Remove Header from App.tsx</name>
  <files>frontend/src/App.tsx</files>
  <action>
    Remove the `<header>` element and its contents ("Transit Dashboard") from the App component.
  </action>
  <verify>
    Check frontend/src/App.tsx to ensure the header tag is gone.
  </verify>
  <done>
    App.tsx no longer contains the header element.
  </done>
</task>

<task type="auto">
  <name>Task 2: Remove Sidebar and Fix Layout in App.css</name>
  <files>frontend/src/App.css</files>
  <action>
    - Remove the `@media (min-width: 900px)` rule that sets `grid-template-columns: 1fr 350px` for the `main` element.
    - Update the `main` element style to only use a single column layout (`grid-template-columns: 1fr`).
    - Adjust `min-height` of `.hero-container` to `100vh` (since header is removed).
  </action>
  <verify>
    Check frontend/src/App.css for the removal of the 350px column and media query.
  </verify>
  <done>
    App.css updated to a single-column layout without the sidebar.
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries
| Boundary | Description |
|----------|-------------|
| Client UI | Visual layout changes, no security impact |

## STRIDE Threat Register
| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-05-01 | Tampering | Layout | mitigate | CSS changes are static and localized |
</threat_model>

<verification>
Verify that the header is gone and the dashboard/hero search now occupies the full width without a sidebar on large screens.
</verification>

<success_criteria>
- No 'Transit Dashboard' text at the top
- Layout is single-column even on wide screens
</success_criteria>

<output>
After completion, create .planning/phases/05-cleanup/05-01-SUMMARY.md
</output>
