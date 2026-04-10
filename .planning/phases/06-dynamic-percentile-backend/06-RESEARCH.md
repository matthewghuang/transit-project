# Phase 6: Dynamic Percentile Backend - Research

## TimescaleDB Percentile Aggregates
To support high-performance dynamic percentiles (D-03), we must move away from `numpy` in-memory calculations (which require fetching thousands of rows per request) to database-side approximate aggregates using TimescaleDB hyperfunctions.

### Key Functions
- `percentile_agg(delay_seconds)`: Creates a digest of the data distribution.
- `approx_percentile(digest, percentile)`: Extracts a specific percentile from the digest.

### Implementation Pattern
```sql
SELECT 
    approx_percentile(percentile_agg(delay_seconds), 0.5) as median,
    approx_percentile(percentile_agg(delay_seconds), 0.95) as p95,
    count(*) as observation_count
FROM delay_observations
WHERE stop_id = $1
AND observed_at::time >= $2
AND observed_at::time <= $3;
```

## Discrete Percentile Steps & Snapping
D-01 and D-02 require supporting specific steps: 50, 75, 90, 95, 99.

### Snapping Logic
```python
def snap_percentile(p: float) -> float:
    STEPS = [0.5, 0.75, 0.90, 0.95, 0.99]
    return min(STEPS, key=lambda x: abs(x - (p / 100.0)))
```

## Low Data Strategy (D-04)
The API must return a `low_confidence` flag if `observation_count < 10`.

### Response Structure Update
```json
{
  "stop_id": "12345",
  "predicted_time": "14:20:00",
  "confidence": 95,
  "low_confidence": true,
  "observation_count": 4
}
```

## Arrive-By Safety Logic (D-05)
The logic for `arrive_by_time` must be:
`arrive_by_sec = min(sched_sec, sched_sec + percentile_delay_sec)`

Note: `percentile_delay_sec` can be negative (early bus). If the bus is usually 2 minutes early at 95% confidence, `arrive_by_sec` will be `sched_sec - 120`. If it's usually 5 minutes late, `arrive_by_sec` will be `sched_sec` (capped).

## Performance Considerations
- Hyperfunctions like `percentile_agg` are highly optimized but still require scanning the index.
- The `stop_id` + `observed_at::time` index is critical. 
- Using approximate aggregates significantly reduces data transfer between DB and API.

## Checklist for Planning
- [ ] Add `low_confidence` field to Pydantic models.
- [ ] Update `get_delay_distribution` to use TimescaleDB hyperfunctions.
- [ ] Update `get_next_buses` to accept `confidence` param and apply safety cap.
- [ ] Ensure snapping logic is applied to input `confidence`.
