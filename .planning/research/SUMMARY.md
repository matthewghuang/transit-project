# Project Research Summary

**Project:** Translink Delay Distribution Dashboard
**Domain:** Real-time Transit Analytics
**Researched:** 2026-04-09
**Confidence:** HIGH

## Executive Summary

The Translink Delay Distribution Dashboard is a probabilistic transit reliability tool designed to move beyond deterministic "minutes away" arrivals. By analyzing historical GTFS-Realtime (GTFS-R) data against static schedules, the system provides users with arrival probability distributions (PDFs) and confidence-based arrival windows (e.g., "90% chance of arrival by 8:05 AM"). This approach addresses the inherent uncertainty in urban transit, helping users manage risk and plan "worst-case" buffers.

The recommended technical approach leverages **TimescaleDB** for high-performance time-series storage and **FastAPI** for a low-latency statistical API. Data is ingested from Kafka, enriched by joining real-time vehicle positions with static schedule data, and stored as discrete delay observations. This architecture ensures that complex distribution calculations—critical for the dashboard's value proposition—can be performed efficiently even as historical data grows.

The primary risks involve data quality issues inherent in GTFS-R, such as clock drift between the agency and the consumer, "ghost buses" (stale updates), and missing data from cancelled trips. Mitigation strategies include using feed header timestamps for all calculations, implementing "dead man's switches" for missing trips, and strict validation of entity freshness.

## Key Findings

### Recommended Stack

The stack is optimized for high-throughput ingestion and complex statistical queries. **TimescaleDB** is the cornerstone, providing "Hyperfunctions" for efficient percentile and distribution estimation. **FastAPI** provides the performance needed for concurrent distribution requests, while **Python 3.12** offers the necessary statistical libraries (NumPy/SciPy).

**Core technologies:**
- **TimescaleDB (Postgres 17):** Time-series Storage — Provides specialized hyperfunctions for high-accuracy PDF estimation without full table scans.
- **FastAPI:** API Framework — High-performance async capabilities critical for serving CPU-bound distribution curves.
- **Python 3.12 / uv:** Processing & Package Management — Optimal for Kafka consumer logic and managing heavy math dependencies (NumPy/SciPy).

### Expected Features

The project focuses on moving from "real-time tracking" to "reliability forecasting."

**Must have (table stakes):**
- **Real-time "Minutes Away":** Fundamental baseline already partially present in the frontend.
- **Schedule-Join Delay:** Calculating true delay by comparing GTFS-R to `stop_times.txt`.
- **Vehicle Location Map:** Visual confirmation of data to build user trust.

**Should have (competitive):**
- **Delay Probability Distribution (PDF):** The core USP showing arrival likelihood windows.
- **"Worst Case" Buffer Recommendation:** Derived from CDF (e.g., "Be here by X for 95% certainty").
- **Ghost Bus Indicator:** Flagging stale telemetry to maintain data integrity.

**Defer (v2+):**
- **Multi-stop benchmarking:** Comparative analysis across the network.
- **Long-term Trends (>30 days):** Longitudinal analysis once data density is sufficient.

### Architecture Approach

A decoupled architecture separates the heavy-write ingestion layer from the read-heavy analysis API. This allows for independent scaling of Kafka consumers and web workers.

**Major components:**
1. **GTFS Static Loader:** Loads and indexes `stop_times.txt` and `trips.txt` for O(1) lookups.
2. **Real-time Enricher:** Consumes Kafka, joins with static schedule cache, and emits delay events.
3. **Analysis Engine (FastAPI):** Queries historical data and uses SciPy/NumPy for Kernel Density Estimation (KDE).

### Critical Pitfalls

1. **Clock Drift:** Misaligning server time with agency feed time causes systematic bias. **Avoid by:** Using `header.timestamp` as the only reference.
2. **Trip Cancellations:** Ignoring cancelled trips makes reliability look better than it is. **Avoid by:** Recording cancellations as explicit failure events.
3. **Ghost Buses:** Stale data points stretching distribution curves. **Avoid by:** Validating entity timestamps against the feed header.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Data Foundation & Ingestion
**Rationale:** The system cannot function without a high-performance join between static schedules and real-time feeds.
**Delivers:** GTFS Static loader and a Kafka consumer that calculates and stores discrete `delay_seconds`.
**Addresses:** Schedule Join, Real-time Ingestion.
**Avoids:** Clock Drift (by implementing `header.timestamp` logic early).

### Phase 2: Historical Storage & Optimization
**Rationale:** Aggregating millions of observations requires specialized time-series indexing.
**Delivers:** TimescaleDB hypertables and continuous aggregates for time-bucketed delay stats.
**Uses:** TimescaleDB 2.17+ hyperfunctions.
**Implements:** Historical Store component.

### Phase 3: Distribution API & Math
**Rationale:** The core USP (PDFs) requires a dedicated analysis layer to turn raw points into smooth curves.
**Delivers:** FastAPI endpoints for PDF/CDF data and "Worst Case" buffer calculations.
**Addresses:** Delay Probability Distribution (PDF), "Worst Case" Buffer.

### Phase 4: Probabilistic UI Integration
**Rationale:** Users need a way to visualize uncertainty beyond a simple "minutes" countdown.
**Delivers:** React distribution charts and confidence indicators.
**Avoids:** Misinterpreting "On Time" (by defining clear thresholds in the UI).

### Phase Ordering Rationale

- **Dependency-Driven:** Static data must be indexed before real-time enrichment is possible; storage must be optimized before the API can perform performant distribution queries.
- **Architecture Alignment:** Separating ingestion (Phase 1/2) from presentation (Phase 3/4) matches the recommended decoupled architecture.
- **Pitfall Prevention:** Critical data quality logic (Phase 1) is prioritized to ensure the historical record is clean before analysis begins.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Analysis API):** Needs research into Kernel Density Estimation (KDE) bandwidth selection for smooth but accurate transit curves.
- **Phase 1 (Enrichment):** Needs API research into Translink's specific `SCHEDULE_RELATIONSHIP` behavior for cancellations.

Phases with standard patterns (skip research-phase):
- **Phase 2 (Storage):** TimescaleDB transit patterns are well-documented.
- **Phase 4 (UI):** Standard React/Leaflet/D3 patterns for transit maps and histograms.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | TimescaleDB + FastAPI is the industry standard for this domain in 2026. |
| Features | HIGH | Table stakes and differentiators are well-aligned with project goals. |
| Architecture | HIGH | Decoupled ingestion/API pattern is robust and scalable. |
| Pitfalls | HIGH | Common GTFS-R failures are well-documented by MobilityData and Google. |

**Overall confidence:** HIGH

### Gaps to Address

- **Translink Specifics:** How often Translink publishes new static GTFS bundles needs verification to automate Phase 1 updates.
- **Memory Footprint:** The "Schedule-in-Memory" pattern for Translink's size needs validation (estimated ~100MB).

## Sources

### Primary (HIGH confidence)
- `GTFS Realtime Best Practices (gtfs.org)` — Protocols for timestamping and cancellation handling.
- `TimescaleDB Transit Patterns` — Storage optimization strategies for high-frequency transit.
- `PostgreSQL 17 Release Notes` — Performance verification for B-tree and indexing.

### Secondary (MEDIUM confidence)
- `Transit App Blog` — UI/UX patterns for historical reliability.
- `OneBusAway Architecture` — General decoupled pattern for transit engines.

---
*Research completed: 2026-04-09*
*Ready for roadmap: yes*
