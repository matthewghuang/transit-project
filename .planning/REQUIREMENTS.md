# Requirements: Translink Delay Distribution Dashboard

**Defined:** April 10, 2026
**Core Value:** Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

## v1 Requirements (SHIPPED)

These requirements were delivered in Milestone v1.0.

- **CORE-01**: User can select a stop by ID or name in the UI.
- **CORE-02**: User can view a real-time "Minutes Away" countdown for buses arriving at the selected stop.
- **CORE-03**: User can view a live map showing the current position of vehicles incoming to the selected stop.
- **REL-01**: Ingestion consumer calculates schedule deviation by joining real-time position data with static `stop_times.txt`.
- **REL-02**: Historical delay observations are stored in PostgreSQL/TimescaleDB with stop, route, and time-of-day metadata.
- **REL-03**: User can view a Probability Density Function (PDF) curve showing the likelihood of different delay durations for the selected stop/time.
- **REL-04**: User can view a "Typical Delay" summary statistic (e.g., "Usually arrives 2m late").

## Active Requirements (v1.1)

### Search-First Pivot (SRCH)

- **SRCH-01**: User can search for a bus stop by intersection (e.g., "Main & 41st").
- **SRCH-02**: User can search for a bus stop by its unique stop number.
- **SRCH-03**: Backend support for full-text search or fuzzy matching on stop intersections/names.
- **SRCH-04**: Results display showing Scheduled time, Actual (real-time) time, and Predicted (historical) arrival time for the next bus.
- **SRCH-05**: Mobile-optimized search interface with auto-suggest capabilities.

### Advanced Reliability (ADV)

- **ADV-01**: Confidence-based arrival window recommendations (e.g., "Arrive by X for 95% certainty").
- **ADV-02**: "Ghost Bus" detection and UI indicators for stale vehicle updates.
- **ADV-03**: Trip cancellation historical logging and impact analysis.

## Out of Scope / Deferred

- **UIO-03**: Optimize the map interaction for high-density stop areas (REMOVED: Map feature discontinued).
- **CORE-03**: User can view a live map showing the current position of vehicles incoming to the selected stop (REMOVED: Map feature discontinued).
- **UIO-02**: Implement a themeable design system (Dark/Light mode support).

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
| ADV-01 | Phase 5 | Pending |
| ADV-02 | Phase 5 | Pending |
| ADV-03 | Phase 5 | Pending |
| CORE-03 | - | Deferred |
| UIO-01 | Phase 4 | Complete |
| UIO-02 | - | Deferred |
| UIO-03 | - | Deferred |
| UIO-04 | Phase 4 | Complete |

**Coverage:**
- v1 requirements: 6 active, 1 deferred
- v1.1 requirements: 8 active, 2 deferred
- Mapped to phases: 14/14 (active)
- Unmapped: 0 ✓
