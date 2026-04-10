# Translink Delay Distribution Dashboard

## What This Is

A real-time transit dashboard that visualizes the reliability of bus routes at specific stops. Instead of just showing "minutes away," it provides a probability density visualization of how late a bus is likely to be based on historical performance for that specific time of day.

## Core Value

Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

## Requirements

### Validated

- ✓ Real-time GTFS-R ingestion via Kafka — existing `main.py`
- ✓ Vehicle position storage in MongoDB — existing `demo_consumer.py`
- ✓ Basic React/Leaflet frontend — existing `frontend/`

### Active

- [ ] **Ingestion**: New Kafka consumer to calculate schedule deviation (delay) by joining GTFS-R with static `stop_times.txt`.
- [ ] **Storage**: PostgreSQL database to store historical delay observations (stop_id, route_id, delay_seconds, timestamp).
- [ ] **Analysis**: API endpoint to calculate probability density functions (PDF) for delays at a given stop/time.
- [ ] **Visualization**: React component showing a distribution curve of expected delays for the selected stop.

### Out of Scope

- **Predictive ML**: We are using historical frequency distributions, not training a neural network for real-time traffic prediction (initially).
- **Multi-agency support**: Focused exclusively on Translink GTFS data.

## Context

The project leverages an existing Kafka-based pipeline. The `main.py` script acts as a producer, fetching Protobuf data from Translink and pushing it to Kafka. The new feature will run as a parallel consumer, enriching the data with static schedule information to derive "lateness" metrics.

## Constraints

- **Tech Stack**: Python (FastAPI, Confluent Kafka), PostgreSQL (TimescaleDB preferred), React.
- **Data Freshness**: GTFS-R polled every 30 seconds (Translink API limit/preference).
- **Storage**: `stop_times.txt` is ~90MB; historical delay observations will grow significantly over time.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| PostgreSQL | Better suited for relational joins (Stop/Trip/Route) and time-of-day aggregations than MongoDB or InfluxDB. | — Pending |
| Rolling Historical Window | Using historical data for specific time-of-day/day-of-week provides the most relevant "distribution" for users. | — Pending |

---
*Last updated: April 09, 2026 after initialization*
