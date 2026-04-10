# Phase 3: Probabilistic API & Visualization - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-09
**Phase:** 03-probabilistic-api-visualization
**Areas discussed:** Statistical Method, Temporal Windowing, Frontend Visualization, Summary Statistics

---

## Statistical Method

| Option | Description | Selected |
|--------|-------------|----------|
| Simple Histogram | 1-minute buckets, transparent. | ✓ |
| KDE | Smooth Continuous curve. | |
| Aggregate Stats | Mean/StdDev only. | |

**User's choice:** Simple Histogram
**Notes:** Chosen for transparency and ease of implementation.

---

## Temporal Windowing

| Option | Description | Selected |
|--------|-------------|----------|
| Slot-based | 2-hour window around target time. | ✓ |
| Exact Match | Only the specific trip time. | |
| Weighted Recency | Favor recent days. | |

**User's choice:** Slot-based
**Notes:** Provides enough data density for meaningful distributions.

---

## Frontend Visualization

| Option | Description | Selected |
|--------|-------------|----------|
| Area Chart | Shaded curve showing probability mass. | ✓ |
| Probability Bars | Traditional histogram bars. | |
| Bell Curve | Normal distribution overlay. | |

**User's choice:** Area Chart
**Notes:** Provides the most intuitive "cloud of probability" visual.

---

## Summary Statistics

| Option | Description | Selected |
|--------|-------------|----------|
| Median | Resilient "Usually" metric. | ✓ |
| Mode | Most frequent observation. | |
| 90th Percentile | Conservative estimate. | |

**User's choice:** Median
**Notes:** Used for the "Typical Delay" callout.

---

## the agent's Discretion

- Specific React charting library.
- API schema design.
- Opacity and color palette for charts.

## Deferred Ideas

- Buffer time recommendations.
- Stop-to-stop reliability comparison.
