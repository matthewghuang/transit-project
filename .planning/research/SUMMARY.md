# Research Summary: Translink Delay Distribution Dashboard

**Domain:** Real-time Transit Analytics & Reliability
**Researched:** April 09, 2026
**Overall confidence:** HIGH

## Executive Summary

The research confirms that a robust GTFS-R delay analysis system relies on a two-stage pipeline: a high-throughput ingestion stage (Kafka) and a relational, time-series optimized storage stage (PostgreSQL/TimescaleDB). The primary technical challenge is the high-frequency join between real-time vehicle positions (keyed by `trip_id`) and static schedules (keyed by `trip_id` and `stop_id`).

For Translink Vancouver, which updates every 30 seconds, an in-memory schedule cache in the consumer is the recommended pattern to keep latency low. The dashboard value comes from aggregating historical observations into Probability Density Functions (PDF), which requires storing delay metrics as structured floats rather than raw Protobuf blobs.

## Key Findings

**Stack:** Python (FastAPI, Confluent-Kafka), PostgreSQL (TimescaleDB), SciPy for PDF calculation.
**Architecture:** Decoupled Kafka Enricher pattern where real-time data is merged with a static schedule cache before persistence.
**Critical pitfall:** Performing CSV lookups or complex joins in the API layer will lead to 10s+ latency for distribution charts.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Static Foundation** - Load GTFS Static into indexed SQL tables. Essential for all subsequent joins.
2. **Real-time Enrichment** - Build the Kafka consumer to calculate and store `delay_seconds`.
3. **Statistical API** - Implement the KDE/PDF logic to turn raw delay points into a smooth distribution curve.
4. **Distribution Visualization** - Integrate the reliability curve into the React frontend.

**Phase ordering rationale:**
- Ingestion depends on Static data structure. API depends on historical data being populated by the Ingestion layer.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Standard transit analytics stack verified. |
| Features | HIGH | PDF visualization is a proven pattern for reliability analysis. |
| Architecture | HIGH | Decoupled consumer pattern is the industry standard for GTFS-R. |
| Pitfalls | MEDIUM | Scale constraints on Translink API (30s polling) may affect data density. |

## Gaps to Address

- Need to verify if `trip_id` in Translink GTFS-R always maps directly to `stop_times.txt` without complex `trip_update` logic (e.g. added/cancelled trips).
- Determining the optimal historical window (7 days vs 30 days) for "representative" distributions.
