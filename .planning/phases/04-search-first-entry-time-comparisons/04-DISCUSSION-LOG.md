# Phase 4: Search-First Entry & Time Comparisons - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-10
**Phase:** 04-search-first-entry-time-comparisons
**Areas discussed:** Search Experience, Time Triad Display, Map Removal, Landing Page

---

## Search Experience

| Option | Description | Selected |
|--------|-------------|----------|
| Instant Dropdown | Results appear as the user types | ✓ |
| Result List | Users must press Enter to see results | |

**User's choice:** Dropdown immediately.
**Notes:** User also specified fuzzy matching for intersections and auto-detecting 5-digit stop IDs.

---

## Time Triad Display

| Option | Description | Selected |
|--------|-------------|----------|
| Predicted Time Prominent | Unique value prop emphasis | |
| Earliest Time Prominent | Conservative "Arrive By" emphasis | ✓ |

**User's choice:** The earliest of the three times (Scheduled, Actual, Predicted) shown in large text.
**Notes:** Clicking expands to show deltas, confidence levels, and the probability curve.

---

## Landing Page & Cleanup

**Decisions:**
- Large hero search bar on landing.
- Display "Nearby Stops" if location access is granted.
- Show "Recent Searches" for repeat commuters.
- **Map Removal:** User explicitly requested total removal of map code, not just hiding it.

---

## the agent's Discretion

- Precise fuzzy search algorithm implementation.
- UI transition animations for the "Expand" action.
- Location-based stop sorting logic.
