# Architecture Research: GTFS-R Delay Analysis

**Domain:** Real-time Transit Analytics
**Researched:** April 09, 2026
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer (React)                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Map View│  │ PDF Chart│  │Stop Info│  │ Reliability│        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
├───────┴────────────┴────────────┴────────────┴──────────────┤
│                    Application Layer (FastAPI)              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │           Distribution & Statistics Engine          │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                    Data & Ingestion Layer                   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Kafka    │  │ Enricher │  │ Postgres │  │ GTFS     │     │
│  │ (Raw)    │  │ (Delay)  │  │ (Hist)   │  │ Static   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| **GTFS Static Pre-processor** | Loads `stop_times.txt` and `trips.txt` into indexed relational tables. Optimizes for O(1) trip/stop lookup. | Python script using Pandas or SQL `COPY` command into Postgres. |
| **Real-time Enricher** | Consumes raw Protobuf from Kafka, joins with static schedule to calculate `delay_seconds`, and emits "Delay Events". | Python (Confluent-Kafka) consumer using an in-memory or Redis cache of the current schedule. |
| **Historical Store** | Stores millions of delay observations with time-series indexing. | PostgreSQL with **TimescaleDB** extension for hyper-indexing on `(timestamp, stop_id)`. |
| **Aggregation API** | Queries historical distributions, calculates percentiles, and generates Probability Density Functions (PDF). | FastAPI with SciPy/NumPy for kernel density estimation (KDE). |

## Recommended Project Structure

```
src/
├── ingestion/           # Kafka consumers and data enrichment
│   ├── static/          # GTFS Static loaders
│   └── realtime/        # Kafka -> Delay Enrichment -> Postgres
├── api/                 # FastAPI application
│   ├── routes/          # Endpoints for PDF data and stop stats
│   └── analysis/        # Math/Stats for distribution curves
├── shared/              # Shared models (Pydantic) and DB config
└── frontend/            # React + Tailwind + Leaflet (Existing)
```

### Structure Rationale

- **ingestion/:** Separates the heavy "write" load from the "read" API. This allows scaling the Kafka consumer independently of the web server.
- **api/analysis/:** Isolates the statistical logic (KDE, PDF calculation) from the HTTP boilerplate, making it easier to test the math without a running server.

## Architectural Patterns

### Pattern 1: Schedule-in-Memory Cache

**What:** Load the current day's `stop_times` into a hash map (dictionary) keyed by `(trip_id, stop_id)` for the Enricher.
**When to use:** When processing high-frequency GTFS-R updates (every 30s) to avoid constant DB round-trips for the static "expected time".
**Trade-offs:** High memory usage (~100MB for Translink) but extremely fast delay calculation.

### Pattern 2: Time-Bucket Aggregation

**What:** Group delay observations into 15-minute or 1-hour "buckets" for specific days of the week.
**When to use:** When calculating historical reliability for a specific time-of-day.
**Trade-offs:** Faster queries for users; however, buckets must be wide enough to have sufficient data points.

## Data Flow

### Delay Processing Flow

```
[Translink API]
    ↓ (Protobuf)
[Kafka Producer] → [Kafka Topic: raw_gtfs]
    ↓
[Delay Enricher] ← [Static Schedule Cache]
    ↓ (Calculated Delay)
[Postgres (TimescaleDB)]
```

### Request Flow

```
[User selects Stop]
    ↓
[API] → [Query Postgres for historical delays at Stop X]
    ↓
[Analysis Engine] → [Generate PDF/Distribution]
    ↓
[Frontend] → [Render Distribution Curve]
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k users | Single Postgres instance + 1 Kafka consumer. |
| 1k-100k users | Read replicas for Postgres; move PDF calculation to background workers or cache common stops. |
| 100k+ users | Materialized views for distribution stats; distributed Kafka consumer group. |

### Scaling Priorities

1. **First bottleneck:** Joining Real-time TripID with Static StopTimes. *Fix: Use an in-memory lookup table.*
2. **Second bottleneck:** Aggregating 30+ days of historical data for a single stop query. *Fix: Use TimescaleDB continuous aggregates.*

## Anti-Patterns

### Anti-Pattern 1: Live Joins in API
**What people do:** Query the static CSV files directly in the API for every request.
**Why it's wrong:** Extremely slow; `stop_times.txt` is too large for repeated parsing.
**Do this instead:** Pre-load the CSV into a relational database with indexes.

### Anti-Pattern 2: Storing Raw Protobuf as Blob
**What people do:** Save the entire Protobuf message in the database.
**Why it's wrong:** Makes historical analysis impossible without re-parsing everything.
**Do this instead:** Extract only relevant fields (delay, stop_id, timestamp) into structured columns.

## Suggested Build Order

1. **Static Foundation**: Build the loader for `google_transit/*.txt` into Postgres.
2. **The Enricher**: Create the Kafka consumer that joins incoming positions with the static database to calculate delay.
3. **Storage**: Verify TimescaleDB indexing on the `delay_observations` table.
4. **Analysis API**: Build the endpoint that takes a `stop_id` and returns a histogram/PDF.
5. **UI Integration**: Connect the React frontend to the new API.

## Sources

- [OneBusAway Architecture](https://www.onebusaway.org/docs/architecture/)
- [TimescaleDB Transit Patterns](https://timescale.com/blog/how-to-store-and-query-transit-data/)
- [GTFS Realtime Best Practices](https://gtfs.org/realtime/best-practices/)

---
*Architecture research for: Translink Delay Distribution Dashboard*
*Researched: April 09, 2026*
