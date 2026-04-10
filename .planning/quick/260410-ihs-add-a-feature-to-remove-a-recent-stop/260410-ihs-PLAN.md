---
phase: quick
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: ["frontend/src/components/HeroSearch.tsx"]
autonomous: true
requirements: ["UI-RECENT-STOPS-REMOVE"]
must_haves:
  truths:
    - "Users can remove a stop from their recent searches list"
    - "Removing a stop persists across page refreshes"
  artifacts:
    - path: "frontend/src/components/HeroSearch.tsx"
      provides: "Remove button for recent searches"
---

<objective>
Add a 'remove' button to each recent search item in the HeroSearch component to allow users to manage their recent history.

Purpose: Improve user control over the recent searches list.
Output: Updated HeroSearch.tsx with removal functionality.
</objective>

<execution_context>
@/Users/turq/code/transit-data/.opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@frontend/src/components/HeroSearch.tsx
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add remove functionality to HeroSearch recent searches</name>
  <files>frontend/src/components/HeroSearch.tsx</files>
  <action>
    - Add a `handleRemoveRecent` function that takes a `stopId`, filters it out of the `recentSearches` state, and updates `localStorage`.
    - Update the rendering of `recent-tags` to include a remove button (e.g., an '×' icon or text) next to the stop name.
    - Ensure clicking the remove button does NOT trigger the `onSelectStop` action (use `e.stopPropagation()`).
    - Style the remove button to be subtle but accessible.
  </action>
  <verify>
    <automated>grep "handleRemoveRecent" frontend/src/components/HeroSearch.tsx</automated>
  </verify>
  <done>Users can remove items from recent searches and they stay removed after refresh.</done>
</task>

</tasks>

<success_criteria>
- A "remove" button appears for each recent search item.
- Clicking the button removes the item from the UI and localStorage.
- Clicking the remove button doesn't navigate to the stop dashboard.
</success_criteria>

<output>
After completion, create `.planning/quick/260410-ihs-add-a-feature-to-remove-a-recent-stop/260410-ihs-SUMMARY.md`
</output>
