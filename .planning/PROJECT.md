# Translink Delay Distribution Dashboard

## What This Is

A real-time transit dashboard that visualizes the reliability of bus routes at specific stops. Instead of just showing "minutes away," it provides a probability density visualization of how late a bus is likely to be based on historical performance for that specific time of day.

## Core Value

Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

## Current Milestone: v1.3 Multi-Bus Stop Carousel

**Goal:** Support stops served by multiple routes with a mobile-first horizontal carousel of arrival cards.

**Target features:**
- Backend API update: `/api/stops/{id}/next_buses` returns one upcoming bus per unique route.
- Horizontal Carousel UI: A swipeable row of "Time Triad" cards for mobile-first navigation.
- Component Reuse: Each card retains the full Phase 7 reliability toolset (Chart + Slider).

## Requirements

### Validated

- ✓ Real-time GTFS-R ingestion via Kafka — v1.0
- ✓ Schedule-aware delay calculation engine (in-memory schedule join) — v1.0
- ✓ TimescaleDB historical storage with hypertable optimization — v1.0
- ✓ Probabilistic API endpoint providing delay distributions — v1.0
- ✓ Frontend visualization with Recharts area charts — v1.0
- ✓ Stop-centric UI with arrival countdowns and markers — v1.0
- ✓ Search-first UX with intersection and 5-digit ID support — v1.1
- ✓ Real-time staleness (Ghost Bus) detection — v1.1
- ✓ Trip cancellation logging and consumer detection — v1.1
- ✓ Dynamic confidence intervals with backend API support — v1.2
- ✓ Interactive Radix UI Slider with zero-latency visual feedback — v1.2
- ✓ Dynamic chart shading and Arrive-By safety logic — v1.2

### Active

- [ ] **MULT-01**: Backend API update to return arrivals for all unique routes at a stop
- [ ] **MULT-02**: Horizontal Carousel UI for navigating multiple bus arrival cards
- [ ] **MULT-03**: Refactor TimeTriad to work within a carousel item context

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
*Last updated: April 10, 2026 after milestone v1.3 initialization*
