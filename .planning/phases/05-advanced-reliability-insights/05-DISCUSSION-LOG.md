# Phase 5: Advanced Reliability Insights - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-10
**Phase:** 05-advanced-reliability-insights
**Areas discussed:** Confidence Windows, Ghost Bus Detection, Cancellation Tracking

---

## Reliability Insights

**Decisions:**
- **Confidence Windows:** Use a 95% threshold for "Arrive By" recommendations.
- **Ghost Buses:** Define as updates older than 5 minutes.
- **Cancellations:** Differentiate between delay and explicit trip cancellation in the database.

---

## the agent's Discretion

- Percentile calculation algorithm (interpolated vs discrete).
- Threshold tuning for different route types (Express vs Local).
