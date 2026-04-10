# Roadmap: Translink Delay Distribution Dashboard

## Milestones

- ✅ **v1.0 Foundation & Probabilistic Insights** — Phases 1-3 (shipped 2026-04-10)
- 📋 **v1.1 Advanced Reliability** — Phases 4-5 (planned)

## Phases

<details>
<summary>✅ v1.0 Foundation & Probabilistic Insights (Phases 1-3) — SHIPPED 2026-04-10</summary>

- [x] Phase 1: Real-time Data Foundation (4/4 plans) — completed 2026-04-10
- [x] Phase 2: Historical Storage & Infrastructure (2/2 plans) — completed 2026-04-10
- [x] Phase 3: Probabilistic API & Visualization (3/3 plans) — completed 2026-04-10

</details>

### 📋 v1.1 Advanced Reliability (Planned)

- [ ] **Phase 4: Search-First Entry & Time Comparisons** - Replace the map with a high-intent search box and comprehensive arrival time comparisons.
- [ ] **Phase 5: Advanced Reliability Insights** - Implement "Ghost Bus" detection and confidence-based arrival recommendations.

## Phase Details

### Phase 4: Search-First Entry & Time Comparisons
**Goal**: Transition to a search-centric UX that provides immediate value through multi-dimensional arrival times.
**Depends on**: Phase 3
**Requirements**: SRCH-01, SRCH-02, SRCH-03, SRCH-04, SRCH-05, UIO-01, UIO-04
**Success Criteria** (what must be TRUE):
  1. Users can find a stop by intersection (e.g., "Broadway & Cambie") or 5-digit stop number.
  2. The map is removed from the interface to reduce load time and visual clutter.
  3. Every search result displays a side-by-side comparison of Scheduled vs. Actual vs. Predicted (Historical) time.
  4. The search interface is primary and optimized for one-handed mobile use.
**Plans**: 6 plans
- [x] 04-01-PLAN.md — Backend Search & Schema Cleanup
- [x] 04-02-PLAN.md — Frontend Map Removal & Hero UI
- [x] 04-03-PLAN.md — Stop Dashboard & Time Triad
- [x] 04-04-PLAN.md — UAT Gap Closure (Search & UI)
- [x] 04-05-PLAN.md — Phase 4 Polish & Gap Closure
- [x] 04-06-PLAN.md — UAT Final Fixes (Centering & Data)
**UI hint**: yes

### Phase 5: Advanced Reliability Insights
**Goal**: Expand the analytical depth of the dashboard with predictive windows and anomaly detection.
**Depends on**: Phase 4
**Requirements**: ADV-01, ADV-02, ADV-03
**Success Criteria** (what must be TRUE):
  1. Users see a recommended "arrival window" with a configurable confidence level (e.g., 95%).
  2. The UI clearly flags vehicles that have not updated in >2 minutes as "Stale/Ghost".
  3. Historical trip cancellations are factored into the reliability visualization.
**Plans**: TBD
**UI hint**: yes

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Real-time Data Foundation | v1.0 | 4/4 | Complete | 2026-04-10 |
| 2. Historical Storage & Infrastructure | v1.0 | 2/2 | Complete | 2026-04-10 |
| 3. Probabilistic API & Visualization | v1.0 | 3/3 | Complete | 2026-04-10 |
| 4. Search-First Entry & Time Comparisons | v1.1 | 0/0 | Not started | - |
| 5. Advanced Reliability Insights | v1.1 | 0/0 | Not started | - |

---
*Last updated: April 10, 2026 after v1.0 milestone completion*
