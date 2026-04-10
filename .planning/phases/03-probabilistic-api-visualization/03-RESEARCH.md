# Phase 3 Research: Probabilistic API & Visualization

## Domain Analysis
Phase 3 transitions the project from "what is happening now" to "what usually happens". This requires statistical aggregation of historical delay observations.

### Data Source
- Table: `delay_observations` (Hypertable)
- Columns: `observed_at`, `stop_id`, `route_id`, `trip_id`, `delay_seconds`
- Aggregates: `hourly_delay_stats` (Continuous Aggregate) provides avg, stddev, and p95.

### Implementation Patterns
- **Backend**: FastAPI with `asyncpg`. Use `NumPy` for server-side processing of raw observations if complex bucketing is needed beyond SQL capabilities.
- **Frontend**: React with Zustand. A new charting library (likely `Recharts`) needs to be added.

## Statistical Approach
Per D-01, we will use histograms.
- **SQL**: Query `delay_observations` for a specific `stop_id` and temporal window.
- **Bucketing**: Use `width_bucket` in PostgreSQL or `numpy.histogram` in Python to create 1-minute intervals.
- **Temporal Window**: 2-hour sliding window (centered on current time) partitioned by Weekday/Weekend (D-03).

## Visual Approach
Per D-04, we will use an Area Chart.
- **Library**: `Recharts` (chosen for its composability and alignment with the current React setup).
- **Component**: `DelayDistributionChart.tsx` will consume the API and render the likelihood mass.

## Security Considerations (STRIDE)
- **Information Disclosure**: Ensure `trip_id` or other internal identifiers aren't leaked if not needed.
- **Denial of Service**: Aggregation queries on large datasets can be heavy. Use indexes and TimescaleDB continuous aggregates where possible.

## Key Blocker/Risks
- **Data Volume**: If a stop has thousands of observations, the query might be slow.
- **Charting Performance**: Rendering complex area charts with many points.

