# Phase 7: Interactive Confidence UI - Context

**Gathered:** 2026-04-10
**Status:** Ready for planning

<domain>
## Phase Boundary

Commuters can dynamically adjust and visualize their preferred reliability threshold. This phase delivers an interactive slider that controls the "Arrive-By" confidence level, with real-time visual feedback on the delay distribution chart.

</domain>

<decisions>
## Implementation Decisions

### Slider Placement
- **D-01:** The confidence slider will live inside the expanded Time Triad view (revealed after clicking a stop and its hero time).
- **D-02:** It will be positioned above or below the delay distribution chart for clear contextual relevance.

### Chart Highlighting
- **D-03:** The chart will visually represent the selected confidence level by shading the area under the probability curve corresponding to that percentile.
- **D-04:** As the user slides, the shaded area will expand or contract in real-time.

### Update Latency
- **D-05:** The "Arrive-By" time in the Time Triad must update instantly as the user moves the slider.
- **D-06:** Use a local estimate based on the histogram data already present in the chart component for zero-latency feedback.
- **D-07:** Perform a debounced sync with the backend API (Phase 6) once the user finishes sliding to ensure long-term precision.

### the agent's Discretion
- The exact visual style of the slider (Radix UI Slider recommended).
- The specific color palette for the shaded area vs. the background chart.
- The wording of the confidence level labels (e.g. "Arrive by X (95% certainty)").

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Core UI Requirements
- `.planning/REQUIREMENTS.md` — Requirements CONF-01, CONF-02, and CONF-03.
- `.planning/phases/06-dynamic-percentile-backend/06-CONTEXT.md` — Backend support for dynamic confidence levels.

### Existing UI Code
- `frontend/src/components/TimeTriad.tsx` — The interaction host.
- `frontend/src/components/DelayDistributionChart.tsx` — The visualization host.

[No external specs — requirements fully captured in decisions above]

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `recharts` — Already used for the delay distribution area chart.
- `Zustand` — Used for state management; consider adding a `confidenceLevel` slice to `filterStore.ts`.

### Established Patterns
- Component-level state for expansion.
- React Query for data fetching (can be extended with the new confidence param).

### Integration Points
- `filterStore.ts`: Add `confidenceLevel` (default 95%).
- `DelayDistributionChart.tsx`: Update to receive and visualize the current confidence mass.
- `TimeTriad.tsx`: Update to display the slider and handle instant/synced time updates.

</code_context>

<specifics>
## Specific Ideas

- "I want the Arrive-By time to move as I slide, so I can see the tradeoff between sleeping longer and missing my bus."
- Use a shaded area rather than just a line, as it better communicates the idea of "probability mass."

</specifics>

<deferred>
## Deferred Ideas

- **CONF-04: Plain-English Labels:** ("Living Dangerously") deferred to v2.

</deferred>

---

*Phase: 07-interactive-confidence-ui*
*Context gathered: 2026-04-10*
