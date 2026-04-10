# Phase 6: Dynamic Percentile Backend - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-10
**Phase:** 06-dynamic-percentile-backend
**Areas discussed:** Percentile Granularity, Calculation Method, Low Data Strategy

---

## Percentile Granularity

| Option | Description | Selected |
|--------|-------------|----------|
| Discrete steps | 50, 75, 90, 95, 99 (Enables caching and consistency) | ✓ |
| Continuous | Any floating-point 0-100 (Higher precision, harder to cache) | |

**User's choice:** let's do discrete steps
**Notes:** User preferred the standard discrete intervals to ensure predictability and caching potential.

---

## Calculation Method

| Option | Description | Selected |
|--------|-------------|----------|
| Approximate (percentile_agg) | Faster and more scalable for TimescaleDB. (Recommended) | ✓ |
| Exact (percentile_cont) | Mathematically exact but slower on large datasets. | |

**User's choice:** Approximate (percentile_agg)
**Notes:** Performance was prioritized over mathematical absolute precision, which is appropriate for transit estimates.

---

## Low Data Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| 10 observations | Standard for simple statistics. (Recommended) | ✓ |
| 5 observations | Better for low-frequency routes. | |
| 25 observations | Stricter, more reliable. | |

**User's choice:** it should warn the user, 10 observations threshold
**Notes:** The system will flag responses with low sample counts so the UI can communicate the lower reliability to the commuter.

---

## the agent's Discretion

- Exact JSON structure for the low-confidence flag.
- Implementation of the "snap to nearest" logic for requested percentiles.

## Deferred Ideas

- Visualizing the highlight region on the chart (deferred to Phase 7).
- Plain-English risk labels (deferred to v2).
