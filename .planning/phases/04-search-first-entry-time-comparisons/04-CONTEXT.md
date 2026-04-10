# Phase 4: Search-First Entry & Time Comparisons - Context

**Gathered:** 2026-04-10
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase involves a complete overhaul of the frontend user interface. The existing map-based navigation will be removed and replaced with a search-centric entry point. The primary interaction flow will be: Search (Intersection/Stop #) -> Stop Dashboard -> Time Triad visualization.

</domain>

<decisions>
## Implementation Decisions

### Search Experience
- **D-01: Instant Dropdown.** Results must appear in an auto-suggest dropdown as the user types.
- **D-02: Fuzzy Matching.** Intersection search (e.g., "Main & 41st") must support fuzzy matching to handle variations in naming.
- **D-03: Numeric Prioritization.** If the input is exactly a 5-digit number, it must be prioritized as a Stop ID and ideally jump directly to that stop.
- **D-04: Recent Searches.** The UI will store and display the last 3–5 searched stops locally for quick access.
- **D-05: Hero Landing.** The initial landing page will feature a large, centered search bar.
- **D-06: Nearby Stops.** If location permission is granted, the closest 3 stops will be displayed as quick-action buttons below the search bar.

### The "Time Triad" Display
- **D-07: Hero Time (Earliest First).** The dashboard will display a single prominent "Hero" time, which is the earliest of the three available values (Scheduled, Actual, or Predicted).
- **D-08: Time Labeling.** The hero time must be clearly labeled with its source (e.g., "5m - Actual").
- **D-09: Dashboard Layout.** The stop view will be a single-stop dashboard (not a list of many stops).
- **D-10: Expanded View.** Clicking the hero time expands the view to show:
    - The full triad (Scheduled, Actual, Predicted) with specific deltas (e.g., "2m behind schedule").
    - The Probability Density Function (PDF) curve from Phase 3.
    - Confidence levels (e.g., "95% certain").
- **D-11: No Status Indicators.** No flashing, pulsing, or specific "ARRIVING" text status indicators; the focus remains on the time values.

### Technical Cleanup
- **D-12: Full Map Removal.** All Leaflet dependencies, map components, and map-specific state logic (e.g., `usePositions.ts` if only used for the map) will be deleted from the codebase to optimize bundle size.

### the agent's Discretion
- Debounce timing for the fuzzy search (suggested 300ms).
- Exact visual design of the Time Triad cards and the "Expand" transition.
- Backend implementation of fuzzy matching (PostgreSQL `pg_trgm` or similar).

</decisions>

<specifics>
## Specific Ideas

- "It should show one time in big. The earliest time between the three."
- "A large hero search as well as nearby stops."
- Users should feel like they can find their stop in seconds, without having to navigate a map.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Transit Data Specs
- `google_transit/` — GTFS static structures used for stop searching.
- `.planning/REQUIREMENTS.md` — Specifically SRCH-01 through SRCH-06.

### Architectural Decisions
- `.planning/PROJECT.md` — For core value alignment on "probabilistic insights."

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `NextBusesDisplay.tsx`: Needs major refactoring to handle the new "Hero Time" logic and expansion.
- `useStops.ts`: Can be extended to support the new fuzzy search backend endpoint.
- `filterStore.ts`: Needs to be updated to remove map-related filters and focus on `selectedStopId`.

### Established Patterns
- Recharts (used in Phase 3) will be used in the expanded "Triad" view to show the probability curve.

### Integration Points
- New API endpoint needed: `GET /api/stops/search?q=...` supporting intersection and ID search.

</code_context>

<deferred>
## Deferred Ideas

- **UIO-02: Dark Mode.** Theme support remains deferred.
- **ADV-01/02:** "Ghost Bus" and "Confidence Windows" are reserved for Phase 5.

</deferred>

---

*Phase: 04-search-first-entry-time-comparisons*
*Context gathered: 2026-04-10*
