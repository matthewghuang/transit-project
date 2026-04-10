# Translink Delay Distribution Dashboard

## What This Is

A real-time transit dashboard that visualizes the reliability of bus routes at specific stops. Instead of just showing "minutes away," it provides a probability density visualization of how late a bus is likely to be based on historical performance for that specific time of day.

## Core Value

Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

## Requirements

### Validated

- ✓ Real-time GTFS-R ingestion via Kafka — v1.0
- ✓ Schedule-aware delay calculation engine (in-memory schedule join) — v1.0
- ✓ TimescaleDB historical storage with hypertable optimization — v1.0
- ✓ Probabilistic API endpoint providing delay distributions — v1.0
- ✓ Frontend visualization with Recharts area charts — v1.0
- ✓ Stop-centric UI with arrival countdowns and markers — v1.0

### Active

- [ ] **ADV-01**: Confidence-based arrival window recommendations (e.g., "Arrive by X for 95% certainty").
- [ ] **ADV-02**: "Ghost Bus" detection and UI indicators for stale vehicle updates.
- [ ] **ADV-03**: Trip cancellation historical logging and impact analysis.
- [ ] **REL-04**: Enhanced "Typical Delay" summary statistics (e.g., "Usually arrives 2m late").

### Out of Scope

- **Predictive ML**: We are using historical frequency distributions (KDE-lite), not training a neural network for real-time traffic prediction.
- **Multi-agency support**: Focused exclusively on Translink GTFS data.
- **User Accounts**: Not needed for core visualization value.

## Context

Shipped v1.0 with a complete ingestion, storage, and visualization pipeline.
Tech stack: Python 3.13, FastAPI, Kafka, TimescaleDB, React 19.
The system now calculates delays by joining real-time `TripUpdate` messages with static schedules and visualizes the likelihood of lateness for commuters.

## Constraints

- **Tech Stack**: Python (FastAPI, Confluent Kafka), TimescaleDB, React.
- **Data Freshness**: GTFS-R polled every 30 seconds.
- **Storage**: `stop_times.txt` is ~90MB; historical delay observations stored in TimescaleDB hypertables.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| TimescaleDB | Efficiently handles time-series delay observations while allowing relational joins with GTFS static data. | ✓ Good |
| In-memory Schedule Lookup | Pandas-based lookup for `stop_times.txt` provides O(1) performance during real-time enrichment. | ✓ Good |
| Batch SQL Persistence | Buffering observations in-memory and using `copy_records_to_table` prevents database bottlenecks. | ✓ Good |
| Area Chart Visualization | Provides an intuitive visual representation of probability density for commuters. | ✓ Good |

---
*Last updated: April 10, 2026 after v1.0 Foundation & Probabilistic Insights milestone completion*
