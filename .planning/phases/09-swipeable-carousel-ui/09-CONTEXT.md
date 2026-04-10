# Phase 9: Swipeable Carousel UI - Context

**Gathered:** 2026-04-10
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement a mobile-first, swipeable horizontal carousel for displaying multiple bus arrival cards at a stop. This phase includes refactoring `TimeTriad` and `StopDashboard` to handle an array of arrivals, adding a global confidence slider, and implementing the carousel mechanics (touch for mobile, arrows for desktop).

</domain>

<decisions>
## Implementation Decisions

### Carousel Implementation
- **D-01:** Use **Embla Carousel** for the carousel logic. It provides the right balance of lightweight footprint and excellent touch/desktop arrow support.
- **D-02:** Use **Partial Peek** layout (e.g., 1.1 or 1.2 cards visible) to visually signal to users that the content is swipeable.
- **D-03:** Add **Navigation Arrows** for desktop users while relying on native touch swiping for mobile.

### Control Scope
- **D-04:** Implement a **Global Slider** for confidence. Instead of a slider per card, one slider will be positioned at the top of the carousel section and its value will apply to all cards simultaneously.

### Component Refactoring
- **D-05:** Refactor `TimeTriad` to accept arrival data as a prop rather than fetching it internally, enabling its reuse inside the carousel.
- **D-06:** Refactor `StopDashboard` to orchestrate the data fetching for the multi-bus array and pass it to the carousel.

### the agent's Discretion
- **D-07:** Exact visual styling of arrows and dots.
- **D-08:** Handling of the "Expanded" state in a carousel context (e.g., whether to expand within the carousel or use a modal/overlay).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Components
- `frontend/src/components/TimeTriad.tsx` — Base component to be refactored.
- `frontend/src/components/StopDashboard.tsx` — Main container for the carousel.

### State & Hooks
- `frontend/src/stores/filterStore.ts` — Global confidence level state.
- `frontend/src/hooks/useNextBuses.ts` — Hook providing the multi-route data.

### Docs
- `https://www.embla-carousel.com/` — Embla Carousel documentation.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `useFilterStore`: Already manages the global `confidenceLevel`.
- `DelayDistributionChart`: Can be rendered inside each card to show route-specific reliability.

### Established Patterns
- React Query for data fetching.
- CSS-in-JS (inline styles/App.css) for layout.

### Integration Points
- `StopDashboard`: The primary entry point for stop details where the carousel will live.

</code_context>

<specifics>
## Specific Ideas

- "Arrows should be used on desktop, touch is fine for mobile."
- "Confidence slider should affect all cards."
- Goal is a "swish" mobile-friendly feel.

</specifics>

<deferred>
## Deferred Ideas

- **Carousel Filtering**: Filtering the carousel items by route or direction (v2).
- **Route Icons**: Custom branding/icons for different routes (v1.4).

</deferred>

---

*Phase: 09-swipeable-carousel-ui*
*Context gathered: 2026-04-10*
