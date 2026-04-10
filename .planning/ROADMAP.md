# Roadmap: Translink Delay Distribution Dashboard

## Milestones

- ✅ **v1.0 Foundation & Probabilistic Insights** — Phases 1-3 (shipped 2026-04-10)
- ✅ **v1.1 Advanced Reliability** — Phases 4-5 (shipped 2026-04-10)
- ✅ **v1.2 Dynamic Confidence & Arrive-By Times** — Phases 6-7 (shipped 2026-04-10)
- 🚧 **v1.3 Multi-Bus Stop Carousel** — Phases 8-9 (current)

## Phases

<details>
<summary>✅ v1.0 Foundation & Probabilistic Insights (Phases 1-3) — SHIPPED 2026-04-10</summary>

- [x] Phase 1: Real-time Data Foundation (4/4 plans) — completed 2026-04-10
- [x] Phase 2: Historical Storage & Infrastructure (2/2 plans) — completed 2026-04-10
- [x] Phase 3: Probabilistic API & Visualization (3/3 plans) — completed 2026-04-10

</details>

<details>
<summary>✅ v1.1 Advanced Reliability (Phases 4-5) — SHIPPED 2026-04-10</summary>

- [x] Phase 4: Search-First Entry & Time Comparisons (10/10 plans) — completed 2026-04-10
- [x] Phase 5: Advanced Reliability Insights (1/1 plans) — completed 2026-04-10

</details>

<details>
<summary>✅ v1.2 Dynamic Confidence & Arrive-By Times (Phases 6-7) — SHIPPED 2026-04-10</summary>

- [x] Phase 6: Dynamic Percentile Backend (1/1 plans) — completed 2026-04-10
- [x] Phase 7: Interactive Confidence UI (1/1 plans) — completed 2026-04-10

</details>

<details open>
<summary>🚧 v1.3 Multi-Bus Stop Carousel (Phases 8-9) — CURRENT</summary>

- [x] **Phase 8: Multi-Route Backend API** - Endpoint returns next buses for all unique routes at a stop
- [ ] **Phase 9: Swipeable Carousel UI** - Mobile-first navigation for multiple arrival cards

</details>

## Phase Details

### Phase 8: Multi-Route Backend API
**Goal**: Endpoint returns next buses for all unique routes at a stop
**Depends on**: Phase 7
**Requirements**: MULT-01
**Success Criteria** (what must be TRUE):
  1. `/api/stops/{id}/next_buses` returns an array of unique route arrivals.
  2. The response includes scheduled, actual, and predicted times for each route.
**Plans**: 1 plan
- [x] 08-01-PLAN.md — Refactor API for multi-route arrival support

### Phase 9: Swipeable Carousel UI
**Goal**: Mobile-first navigation for multiple arrival cards
**Depends on**: Phase 8
**Requirements**: MULT-02, MULT-03
**Success Criteria** (what must be TRUE):
  1. Arrival cards are displayed in a horizontal, swipeable row on mobile.
  2. Each card functions as a standalone TimeTriad with confidence controls.
**Plans**: 3 plans
- [ ] 09-01-PLAN.md — Core Refactor & Data Orchestration
- [ ] 09-02-PLAN.md — Embla Carousel Implementation
- [ ] 09-03-PLAN.md — Global Controls & Final Polish

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Real-time Data Foundation | v1.0 | 4/4 | Complete | 2026-04-10 |
| 2. Historical Storage & Infrastructure | v1.0 | 2/2 | Complete | 2026-04-10 |
| 3. Probabilistic API & Visualization | v1.0 | 3/3 | Complete | 2026-04-10 |
| 4. Search-First Entry & Time Comparisons | v1.1 | 10/10 | Complete | 2026-04-10 |
| 5. Advanced Reliability Insights | v1.1 | 1/1 | Complete | 2026-04-10 |
| 6. Dynamic Percentile Backend | v1.2 | 1/1 | Complete | 2026-04-10 |
| 7. Interactive Confidence UI | v1.2 | 1/1 | Complete | 2026-04-10 |
| 8. Multi-Route Backend API | v1.3 | 1/1 | Complete | 2026-04-10 |
| 9. Swipeable Carousel UI | v1.3 | 0/3 | In Progress | - |

---
*Last updated: April 10, 2026 after reconciling Phase 08 completion and Phase 09 planning*
