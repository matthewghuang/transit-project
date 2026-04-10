# Requirements: Translink Delay Distribution Dashboard

**Defined:** April 09, 2026
**Core Value:** Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

## v1 Requirements

Requirements for initial release focusing on the core ingestion pipeline and basic distribution visualization.

### Core Tracking (CORE)

- [ ] **CORE-01**: User can select a stop by ID or name in the UI.
- [ ] **CORE-02**: User can view a real-time "Minutes Away" countdown for buses arriving at the selected stop.
- [ ] **CORE-03**: User can view a live map showing the current position of vehicles incoming to the selected stop.

### Reliability Analysis (REL)

- [ ] **REL-01**: Ingestion consumer calculates schedule deviation by joining real-time position data with static `stop_times.txt`.
- [x] **REL-02**: Historical delay observations are stored in PostgreSQL/TimescaleDB with stop, route, and time-of-day metadata.
- [ ] **REL-03**: User can view a Probability Density Function (PDF) curve showing the likelihood of different delay durations for the selected stop/time.
- [ ] **REL-04**: User can view a "Typical Delay" summary statistic (e.g., "Usually arrives 2m late").

## v2 Requirements

Deferred to future release.

### Advanced Reliability (ADV)

- **ADV-01**: Confidence-based arrival window recommendations (e.g., "Arrive by X for 95% certainty").
- **ADV-02**: "Ghost Bus" detection and UI indicators for stale vehicle updates.
- **ADV-03**: Trip cancellation historical logging and impact analysis.
- **ADV-04**: Multi-stop comparison (e.g., "Is Stop A more reliable than Stop B for this route?").

## Out of Scope

| Feature | Reason |
|---------|--------|
| Predictive ML Models | Using historical statistical distributions (KDE) is sufficient for v1; avoids ML complexity. |
| Multi-Agency Support | Focused exclusively on Translink data for initial scope. |
| User Accounts | Not needed for core visualization value; keep v1 frictionless. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Pending |
| CORE-02 | Phase 1 | Pending |
| CORE-03 | Phase 1 | Pending |
| REL-01 | Phase 1 | Pending |
| REL-02 | Phase 2 | Complete |
| REL-03 | Phase 3 | Pending |
| REL-04 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 7 total
- Mapped to phases: 7
- Unmapped: 0 ✓

---
*Requirements defined: April 09, 2026*
*Last updated: April 09, 2026 after initial definition*
