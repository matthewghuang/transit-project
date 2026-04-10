# Roadmap: Translink Delay Distribution Dashboard

## Phases

- [ ] **Phase 1: Real-time Data Foundation** - Establish the core ingestion pipeline that calculates delays by joining real-time positions with static schedules.
- [x] **Phase 2: Historical Storage & Infrastructure** - Set up the optimized PostgreSQL/TimescaleDB storage for long-term delay observations. (completed 2026-04-10)
- [ ] **Phase 3: Probabilistic API & Visualization** - Implement the statistical analysis engine and the user-facing distribution dashboard.

## Phase Details

### Phase 1: Real-time Data Foundation
**Goal**: Establish a high-performance join between static schedules and real-time feeds to derive discrete delay metrics.
**Depends on**: Nothing
**Requirements**: REL-01, CORE-01, CORE-02, CORE-03
**Success Criteria** (what must be TRUE):
  1. The system can successfully load and index `stop_times.txt` for rapid lookup.
  2. A Kafka consumer correctly identifies the "next stop" for a vehicle and calculates lateness in seconds relative to the static schedule.
  3. The frontend displays a real-time "Minutes Away" countdown and live vehicle positions for a user-selected stop.
**Plans**: 4 plans
- [x] 01-01-PLAN.md — Implement backend ingestion and delay calculation
- [x] 01-02-PLAN.md — Update API and Frontend to visualize delays
- [x] 01-03-PLAN.md — Refine next-stop logic (Gap Closure)
- [x] 01-04-PLAN.md — Implement stop-selection and countdown UI (Gap Closure)
**UI hint**: yes

### Phase 2: Historical Storage & Infrastructure
**Goal**: Persist delay observations in a scalable time-series database optimized for longitudinal analysis.
**Depends on**: Phase 1
**Requirements**: REL-02
**Success Criteria** (what must be TRUE):
  1. All delay events from the ingestion consumer are stored in PostgreSQL/TimescaleDB with correct metadata (stop, route, time-of-day).
  2. Database performance remains stable under continuous write load from the real-time enricher.
  3. Storage schema supports efficient time-bucketed queries for historical aggregation.
**Plans**: 2 plans
- [x] 02-01-PLAN.md — Set up TimescaleDB infrastructure and initialize SQL schema
- [x] 02-02-PLAN.md — Migrate consumer to SQL batching and update API to SQL backend

### Phase 3: Probabilistic API & Visualization
**Goal**: Transform raw historical data into actionable probabilistic insights for commuters.
**Depends on**: Phase 2
**Requirements**: REL-03, REL-04
**Success Criteria** (what must be TRUE):
  1. A FastAPI endpoint provides Kernel Density Estimation (KDE) data for a given stop and time window.
  2. The UI renders a smooth probability distribution curve showing arrival likelihoods.
  3. Users can see a "Typical Delay" summary statistic derived from the historical dataset.
**Plans**: 2 plans
- [x] 03-01-PLAN.md — Implement backend API for delay distributions
- [x] 03-02-PLAN.md — Implement frontend area chart visualization
**UI hint**: yes

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Real-time Data Foundation | 0/1 | Not started | - |
| 2. Historical Storage & Infrastructure | 2/2 | Complete   | 2026-04-10 |
| 3. Probabilistic API & Visualization | 0/1 | Not started | - |
