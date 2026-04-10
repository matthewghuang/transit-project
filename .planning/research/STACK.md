# Technology Stack

**Project:** Translink Delay Distribution Dashboard
**Researched:** 2026-04-09
**Confidence:** HIGH

## Recommended Stack

The 2025/2026 standard for high-frequency transit analytics leans heavily on **TimescaleDB** for storage and **FastAPI** for low-latency distribution calculations. While DuckDB is superior for batch OLAP, the need for continuous ingestion from Kafka and real-time "at-stop" queries makes a time-series optimized Postgres the most robust choice.

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **TimescaleDB** | 2.17+ | Time-series Storage | Provides "Hyperfunctions" specifically for high-accuracy percentile and distribution (PDF) estimation at scale without full table scans. For the new dynamic percentile queries, use native `percentile_cont()` or `approx_percentile()`. |
| **PostgreSQL** | 17 | Relational Engine | Necessary for complex joins between real-time `stop_times` and static GTFS `stops.txt`. |
| **FastAPI** | 0.115+ | API Framework | High-performance async capabilities are critical for handling concurrent requests for distribution curves. |
| **Python** | 3.12+ | Processing Language | Optimal for the Kafka consumer logic. |
| **React** | 19.1+ | UI Framework | Recharts for area charts. |
| **@radix-ui/react-slider** | ^1.1.2 | UI Component | Interactive slider for confidence selection. Accessible, customizable, integrates well without a full component library. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **psycopg3** | 3.2+ | DB Driver | Use for async connection pooling to TimescaleDB. Supports native Python types and faster COPY operations for high-volume ingestion. |
| **confluent-kafka** | 2.6+ | Kafka Client | Standard for high-throughput ingestion from the existing `main.py` producer. Essential for reliable exactly-once semantics if needed. |
| **NumPy** | 2.0+ | Distribution Math | Use on the API side if performing Kernel Density Estimation (KDE) outside the database for smoother visualizations. |
| **SciPy** | 1.14+ | Statistical Functions | When advanced smoothing or curve fitting is required for the "Expected Delay" visualization. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **DBeaver / pgAdmin** | Database Inspection | Use to verify TimescaleDB "Continuous Aggregates" are correctly summarizing delay data. |
| **uv** | Package Management | Fast replacement for `pip`. Extremely useful for managing the complex dependencies of NumPy/SciPy. |

## Installation

```bash
# Core Dependencies
uv add "fastapi[standard]" timescale-py psycopg[binary,pool] confluent-kafka

# Data Analysis
uv add numpy scipy pandas

# Dev dependencies
uv add -D pytest ruff mypy
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **TimescaleDB** | **DuckDB** | Use if the workload is strictly local/batch analysis (e.g., generating a monthly report) rather than a live-updating dashboard. |
| **TimescaleDB** | **ClickHouse** | Use if scale exceeds 100M+ observations per day. ClickHouse is faster for raw ingestion but harder to join with relational GTFS data. |
| **FastAPI** | **Go (Gin/Echo)** | Use if the API only serves data and doesn't need Python's statistical library ecosystem (SciPy/NumPy). |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **MongoDB** | Poor performance for range-based time-of-day aggregations and lacks native statistical distribution hyperfunctions. | **TimescaleDB** |
| **InfluxDB (Flux)** | Difficult to join with static relational GTFS data (Stop/Route info). Flux is more complex than SQL for these joins. | **TimescaleDB** |
| **Vanilla Postgres** | Standard B-Tree indexes on `timestamp` columns bloat and slow down as historical data grows. | **TimescaleDB (Hypertables)** |

## Stack Patterns by Variant

**If High Concurrency (>1000 req/s):**
- Use **FastAPI + Redis caching** for the PDF results.
- Because PDF calculations (especially KDE) are CPU-bound; caching the "9:00 AM Monday" distribution for a stop saves significant cycles.

**If Massive Data Retention (>1 Year):**
- Use **TimescaleDB Tiered Storage (S3)** or **Columnar Compression**.
- Because historical delay data is highly compressible; columnar storage can reduce disk footprint by 90%+.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| `psycopg[binary] >= 3.0` | `PostgreSQL >= 12` | Required for native async support in FastAPI. |
| `FastAPI >= 0.110` | `Pydantic >= 2.0` | Significant performance boost for the API layer. |

## Sources

- `timescale_hyperfunctions` — Verified PDF/Percentile estimation capabilities.
- [FastAPI Official Docs](https://fastapi.tiangolo.com/) — Verified high-performance async patterns for 2025.
- [PostgreSQL 17 Release Notes](https://www.postgresql.org/about/news/postgresql-17-released-2937/) — Performance verification.
- Domain Experience — High confidence in SQL-based time-series for transit (High Confidence).

---
*Stack research for: Transit Delay Distribution Dashboard*
*Researched: 2026-04-09*
