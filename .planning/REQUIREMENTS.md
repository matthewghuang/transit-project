# Requirements: Translink Delay Distribution Dashboard

**Defined:** 2026-04-10
**Core Value:** Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

## v1.2 Requirements

Active requirements for the current milestone.

### Confidence UI

- [ ] **CONF-01**: User can select discrete intervals (50%, 75%, 90%, 95%, 99%)
- [ ] **CONF-02**: Saving the selected confidence level in the URL for bookmarking
- [ ] **CONF-03**: When sliding, the area under the existing delay distribution curve highlights

### Core Logic

- [x] **CORE-04**: Backend API calculates dynamic percentile windows based on requested confidence
- [x] **CORE-05**: "Predicted Time" logic overhaul ensures arrive-by recommendations are always at or before the scheduled time

## Previous Requirements (Shipped)

These requirements were delivered in previous milestones (v1.0, v1.1).

### Core (v1.0)
- **CORE-01**: User can select a stop by ID or name in the UI.
- **CORE-02**: User can view a real-time "Minutes Away" countdown for buses arriving at the selected stop.
- **REL-01**: Ingestion consumer calculates schedule deviation by joining real-time position data with static `stop_times.txt`.
- **REL-02**: Historical delay observations are stored in PostgreSQL/TimescaleDB with stop, route, and time-of-day metadata.
- **REL-03**: User can view a PDF curve showing the likelihood of different delay durations for the selected stop/time.
- **REL-04**: User can view a "Typical Delay" summary statistic (e.g., "Usually arrives 2m late").

### Search & Advanced (v1.1)
- **SRCH-01**: User can search for a bus stop by intersection.
- **SRCH-02**: User can search for a bus stop by its unique stop number.
- **SRCH-03**: Backend support for full-text search or fuzzy matching.
- **SRCH-04**: Results display showing Scheduled time, Actual time, and Predicted arrival time.
- **SRCH-05**: Mobile-optimized search interface with auto-suggest capabilities.
- **ADV-01**: Confidence-based arrival window recommendations.
- **ADV-02**: "Ghost Bus" detection and UI indicators.
- **ADV-03**: Trip cancellation historical logging and impact analysis.
- **UIO-01**: [Completed in v1.1]
- **UIO-04**: [Completed in v1.1]

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Confidence UI
- **CONF-04**: Plain-English Labels: Translates percentages into actionable advice (e.g. 50% = "Living Dangerously")

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Continuous/Granular Sliders (e.g., 87.3%) | Statistically meaningless for our data volume and confusing for UX. Prevents backend caching. |
| Map feature / Live Map | REMOVED: Map feature discontinued (CORE-03, UIO-03). |
| Themeable design system | Deferred (UIO-02). |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Complete |
| CORE-02 | Phase 1 | Complete |
| REL-01 | Phase 1 | Complete |
| REL-02 | Phase 2 | Complete |
| REL-03 | Phase 3 | Complete |
| REL-04 | Phase 3 | Complete |
| SRCH-01 | Phase 4 | Complete |
| SRCH-02 | Phase 4 | Complete |
| SRCH-03 | Phase 4 | Complete |
| SRCH-04 | Phase 4 | Complete |
| SRCH-05 | Phase 4 | Complete |
| ADV-01 | Phase 5 | Complete |
| ADV-02 | Phase 5 | Complete |
| ADV-03 | Phase 5 | Complete |
| UIO-01 | Phase 4 | Complete |
| UIO-04 | Phase 4 | Complete |
| CONF-01 | Phase 7 | Pending |
| CONF-02 | Phase 7 | Pending |
| CONF-03 | Phase 7 | Pending |
| CORE-04 | Phase 6 | Complete |
| CORE-05 | Phase 6 | Complete |

**Coverage:**
- v1.2 requirements: 5 total
- Mapped to phases: 21
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-10*
*Last updated: 2026-04-10 after v1.2 planning*
