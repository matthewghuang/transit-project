# Phase 8: Multi-Route Backend API - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-10
**Phase:** 08-multi-route-backend-api
**Areas discussed:** Route Selection, Uniqueness, Sorting

---

## Route Selection

| Option | Description | Selected |
|--------|-------------|----------|
| Every unique route (Recommended) | Return the next bus for every unique route (Recommended for full visibility) | ✓ |
| Limit to N routes | Limit to top N routes (e.g., first 5) | |

**User's choice:** Every unique route (Recommended)
**Notes:** User emphasized displaying "each bus in a card" in a carousel.

---

## Uniqueness Criteria

| Option | Description | Selected |
|--------|-------------|----------|
| Route ID (Recommended) | Differentiate by Route ID (Standard GTFS) | ✓ |
| Route + Headsign | Differentiate by headsign/direction (e.g., 99 Commercial vs 99 UBC) | |

**User's choice:** Route ID (Recommended)
**Notes:** -

---

## Sorting

| Option | Description | Selected |
|--------|-------------|----------|
| Arrival Time (Recommended) | Sort by scheduled arrival time (Recommended for immediate utility) | ✓ |
| Route Number | Sort by route number (e.g., 2, 4, 99) | |

**User's choice:** Arrival Time (Recommended)
**Notes:** -

---

## the agent's Discretion

- Choice of Pydantic model refactoring for lists.
- Performance optimization for route_id joins.

## Deferred Ideas

- Frontend carousel implementation (Phase 9).
- Directional filtering.
