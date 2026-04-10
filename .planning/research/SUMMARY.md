# Project Research Summary

**Project:** Translink Delay Distribution Dashboard
**Domain:** Real-time Transit Analytics / Probabilistic Dashboard
**Researched:** 2026-04-10
**Confidence:** HIGH

## Executive Summary

The project is evolving to version 1.2, introducing dynamic confidence sliders and dynamic percentile calculations. This transforms the dashboard from static real-time tracking to a probabilistic transit reliability tool that helps commuters make informed decisions using dynamic delay distributions. Experts build these systems by pushing heavy analytical calculations down to time-series optimized databases, avoiding network and memory bottlenecks while allowing interactive percentile generation.

The recommended approach leverages TimescaleDB's native continuous or approximate percentiles to serve a FastAPI backend, paired with a React frontend that features a discrete confidence slider and dynamic area chart highlighting. The most critical risk is database and API overloading from recalculating percentiles dynamically during rapid slider interactions. 

This risk can be mitigated by heavily debouncing API requests and using discrete intervals (e.g., 50%, 75%, 90%). Finally, the system must strictly enforce "conservative arrive-by" logic in the backend, capping recommendations at the scheduled arrival time to guarantee users never miss early buses.

## Key Findings

### Recommended Stack

The 2025/2026 standard for high-frequency transit analytics leans heavily on TimescaleDB for storage and FastAPI for low-latency distribution calculations.

**Core technologies:**
- **TimescaleDB (PostgreSQL 17)**: Time-series Storage — Provides continuous aggregate and hyperfunctions (`percentile_cont`, `approx_percentile`) for high-accuracy percentile and distribution estimation dynamically.
- **FastAPI (0.115+)**: API Framework — High-performance async capabilities critical for handling concurrent distribution curve queries.
- **Python 3.12+ / uv**: Processing & Package Management — Optimal for managing backend logic and dependencies.
- **@radix-ui/react-slider (^1.1.2)**: UI Component — Provides accessible, interactive sliders with discrete snapping intervals.

### Expected Features

**Must have (table stakes):**
- **Discrete Confidence Slider UI** — Users need clear, step-based intervals (e.g., 50%, 75%, 90%) for caching and clear UX.
- **Dynamic Percentile API Endpoint** — Backend must compute delay windows dynamically based on the slider state.
- **Conservative Arrive-By Caps** — Recommendations must NEVER be later than the scheduled time to prevent missed early buses.

**Should have (competitive):**
- **Dynamic Chart Highlighting** — Visual feedback showing probability mass highlighting dynamically under the curve.
- **Plain-English Risk Labels** — Translate raw percentages into actionable advice (e.g., "Living Dangerously", "Typical Commute").

**Defer (v2+):**
- **URL State Persistence** — Not essential for the core interactive loop.

### Architecture Approach

The architecture pushes the heavy analytical calculation (percentiles) down to the database to preserve API responsiveness and reduce memory overhead. 

**Major components:**
1. **TimescaleDB Query Layer** — Dynamically computes exact historical delay percentiles utilizing `percentile_cont()` or approximated hyperfunctions.
2. **api.py Endpoints** — Parses the `confidence` query parameter, orchestrates the DB query, and centrally enforces the "never later than scheduled" safety constraint.
3. **Frontend State (filterStore & Hooks)** — Manages user's desired reliability threshold via debounced state synchronization.

### Critical Pitfalls

1. **On-the-fly SQL Percentile Calculation (DB Meltdown)** — Avoid running full dataset sorts per request on millions of rows. Use TimescaleDB approximate percentiles or restrict the time window heavily.
2. **Slider Event Spamming (API Throttling)** — Avoid direct API binding to raw range input `onChange` events. Prevent by using `onChangeEnd` or a strict 300ms debounce.
3. **"Conservative" Over-Correction Logic** — Avoid strictly subtracting late variance causing users to arrive excessively early. Cap the arrive-by recommendation at the scheduled time.
4. **Ignoring Negative Delays** — Avoid failing to account for early departures by ensuring confidence bounds evaluate the early (negative delay) tail of the distribution.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Database & Backend Logic (api.py)
**Rationale:** Core percentile calculation and strict safety constraints must be validated before exposing dynamic data.
**Delivers:** Updated FastAPI endpoints supporting `?confidence=` queries and dynamic SQL percentile aggregations.
**Addresses:** Dynamic Percentile API Endpoint, Conservative Arrive-By Caps.
**Avoids:** "Conservative" Over-Correction Logic, Ignoring Negative Delays.

### Phase 2: Frontend State & Integration
**Rationale:** Safely wiring the new backend API into the React application's state management before developing visual UI components.
**Delivers:** Zustand `filterStore` updates and React Query (`usePositions`) modifications to pass the new confidence parameters safely.
**Uses:** React 19.1+, `usePositions` hook.
**Implements:** Debounced State Synchronization pattern to protect the backend.
**Avoids:** Slider Event Spamming.

### Phase 3: Interactive Confidence UI
**Rationale:** Visual and interactive layer built safely on top of the established backend API and robust state boundaries.
**Delivers:** Discrete confidence slider, plain-english risk labels, and dynamic area chart highlighting.
**Addresses:** Discrete Confidence Slider UI, Dynamic Chart Highlighting, Plain-English Risk Labels.
**Uses:** `@radix-ui/react-slider`.

### Phase Ordering Rationale

- The data layer needs to support dynamic confidence logic first (Phase 1) to guarantee that safety constraints (arrive-by caps) are structurally enforced centrally.
- Frontend state integration (Phase 2) establishes the communication bridge, critically ensuring network requests are debounced to shield the new expensive endpoints.
- The UI controls and visual highlights (Phase 3) are introduced last, reacting to safe, debounced, and tested data streams.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1:** Requires specific optimization checks on TimescaleDB's `percentile_cont()` performance vs. `approx_percentile` to guarantee DB stability.

Phases with standard patterns (skip research-phase):
- **Phase 2 & 3:** Use standard React state management and UI component debouncing integrations.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | TimescaleDB hyperfunctions and FastAPI performance patterns are highly established. |
| Features | HIGH | Clear constraints directly dictating safety (not missing buses). |
| Architecture | HIGH | Standard push-down database analytics paired with debounced UX patterns. |
| Pitfalls | HIGH | Known and highly specific performance risks identified for dynamic percentiles. |

**Overall confidence:** HIGH

### Gaps to Address

- **DB Performance Validation**: Needs validation during Phase 1 if the dataset size mandates migrating to `approx_percentile` or continuous aggregate bucketing over raw `percentile_cont()`.

## Sources

### Primary (HIGH confidence)
- `STACK.md` — TimescaleDB, PostgreSQL, FastAPI recommendations.
- `ARCHITECTURE.md` — Dynamic Percentile Pushdown, Debounced State Sync.
- `PITFALLS.md` — DB Meltdown, Slider Event Spamming, Over-Correction Logic.
- `FEATURES.md` — Table stakes, competitive features, and anti-features.

---
*Research completed: 2026-04-10*
*Ready for roadmap: yes*
