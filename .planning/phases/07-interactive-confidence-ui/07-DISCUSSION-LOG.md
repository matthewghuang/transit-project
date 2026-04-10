# Phase 7: Interactive Confidence UI - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-10
**Phase:** 07-interactive-confidence-ui
**Areas discussed:** Slider Placement, Chart Highlighting, Update Latency

---

## Slider Placement

| Option | Description | Selected |
|--------|-------------|----------|
| In Expanded Triad | Lives where the details are (Recommended) | ✓ |
| Global Dashboard | A persistent setting on the main stop view | |

**User's choice:** "when a user clicks a stop and clicks the time for more details it should live there"
**Notes:** User preferred keeping the control contextual to the expanded detail view to keep the primary dashboard clean.

---

## Chart Highlighting

| Option | Description | Selected |
|--------|-------------|----------|
| Shaded Area Under Curve | The most intuitive for probability mass. (Recommended) | ✓ |
| Vertical Reference Line | A single moving bar. Cleaner but less 'probabilistic'. | |
| Color Change Curve | Change the color of the curve itself. | |

**User's choice:** Shaded Area Under Curve
**Notes:** Shading provides a better visual metaphor for "how much chance am I taking?"

---

## Update Latency

| Option | Description | Selected |
|--------|-------------|----------|
| Instant Local + Sync | Update instantly using local data, sync backend after (Recommended) | ✓ |
| Debounce & Update | Wait for slider to stop, then fetch new data | |

**User's choice:** "instantly update it and then sync with the backend after"
**Notes:** The user prioritized immediate UI feedback. The implementation will use a local estimation based on histogram buckets to shift the Arrive-By time instantly during the drag.

---

## the agent's Discretion

- Visual styling of the slider.
- Color selection for the probability mass shading.
- Exact phrasing of the confidence labels.

## Deferred Ideas

- Risk labels (e.g., "Safe", "Risky") - deferred to v2.
