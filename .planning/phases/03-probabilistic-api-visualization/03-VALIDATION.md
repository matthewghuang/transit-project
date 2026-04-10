# Phase 3 Validation Strategy

## Goal
Verify that the probabilistic API correctly aggregates historical data and the frontend visualizes it accurately.

## Success Criteria (Must-Haves)
1. **API Likelihood Mass**: The `/api/distribution/{stop_id}` endpoint returns a histogram of 1-minute buckets covering at least 90% of the observation range.
2. **Median Accuracy**: The "Typical Delay" summary matches the 50th percentile of the raw data for that window.
3. **Visual Integrity**: The area chart correctly renders the probability density, with axes matching the API data.

## Automated Checks
- **Unit Test (Backend)**: `pytest` checking histogram bucketing logic with mocked SQL results.
- **Integration Test**: `curl` call to endpoint returns valid JSON with `buckets` and `median` fields.
- **Component Test**: Vitest/React Testing Library check if `<DelayDistributionChart />` renders svg elements.

## Manual Verification
- Visual inspection of the area chart on the dashboard for a known busy stop.
- Verify that toggling between Weekday and Weekend data updates the chart correctly.
