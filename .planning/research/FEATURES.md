# Feature Landscape: Dynamic Confidence & Percentiles

**Domain:** Probabilistic Transit Real-Time Dashboard (v1.2)
**Researched:** April 10, 2026

## Table Stakes

Features users expect when given control over probability and confidence models.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Discrete Confidence Slider UI** | Users need clear, understandable intervals (e.g., 50%, 75%, 90%, 95%, 99%) rather than arbitrary floating percentages. | Low | Snapping to specific steps improves UX and enables query caching on the backend. |
| **Dynamic Percentile API Endpoint** | Backend must calculate delay windows on-the-fly based on the user's requested confidence level instead of using static P90 defaults. | Medium | Requires SQL percentile aggregations dynamically queried over existing TimescaleDB delay observations. |
| **Conservative Arrive-By Caps** | Core safety mechanic: Arrive-by recommendations must *never* be later than the scheduled time, regardless of how late the bus usually is. | Low | Prevents commuters from missing early/on-time buses. Logic: `min(scheduled_time, predicted_time)`. |

## Differentiators

Features that set the UX apart by making complex statistical concepts intuitive.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Dynamic Chart Highlighting** | When the user drags the slider, the area under the existing delay distribution curve highlights to visually represent the selected probability mass. | Medium | High visual impact. Requires coordinating React state (Zustand slider value) with Recharts areas. |
| **Plain-English Risk Labels** | Translates percentages into actionable advice (e.g., 50% = "Living Dangerously", 80% = "Typical Commute", 99% = "Can't Miss This"). | Low | Reduces cognitive load for users who don't intuitively grasp statistical percentiles. |
| **URL State Persistence** | If a user finds a confidence level they like (e.g., 95%), saving it in the URL allows bookmarking their specific risk tolerance. | Low | Excellent quality-of-life for daily commuters returning to the same view. |

## Anti-Features

Features to explicitly NOT build to maintain safety and simplicity.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Continuous/Granular Sliders (e.g., 87.3%)** | Statistically meaningless for our data volume and confusing for UX. Prevents backend caching. | Use a discrete, stepped slider with meaningful intervals (50%, 75%, 90%, 95%, 99%). |
| **Late Arrival Recommendations** | Predicting a bus is always late and telling a user to arrive *after* the scheduled time causes missed buses if traffic is unexpectedly clear. | Always cap the "Arrive-By" recommendation at the `scheduled_time`. |

## Feature Dependencies

```
Dynamic Percentile API → Discrete Confidence Slider (Slider requires API support)
Dynamic Percentile API → Conservative Arrive-By Caps (Depends on dynamic percentile values)
Discrete Confidence Slider → Dynamic Chart Highlighting (Visual update driven by slider state)
Existing TimescaleDB → Dynamic Percentile API (Requires existing delay observations)
Existing Recharts Area → Dynamic Chart Highlighting (Builds on top of current viz)
```

## MVP Recommendation

Prioritize the core mechanics of user-driven probability:
1. **Dynamic Percentile API**: Backend logic to serve multiple confidence tiers.
2. **Discrete Confidence Slider**: Frontend control to switch between those tiers.
3. **Conservative Arrive-By Caps**: Crucial logic overhaul to prevent missed buses (cap at schedule).

Defer: 
- **URL State Persistence**: Can be added later.
- **Dynamic Chart Highlighting**: High visual value but not strictly necessary for the core logic. Save for polish if time permits.

## Sources

- Project Context Constraints: "never later, ensuring commuters don't miss early buses"
- Standard UX practices for statistical tools (discrete steps vs continuous sliders).