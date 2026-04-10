# Feature Landscape

**Domain:** Transit Reliability Dashboards
**Researched:** April 09, 2026

## Table Stakes

Features users expect in any modern transit reliability/tracking application. Missing these typically leads to high bounce rates as the core utility is compromised.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Real-time "Minutes Away"** | Fundamental baseline for any transit app. Users need immediate tactical info. | Low | Already exists in `frontend/` but must be synchronized with distribution data. |
| **Stop-Specific Search/Selection** | Reliability is hyper-local; a route may be reliable globally but fail at a specific bottleneck stop. | Low | Core requirement for stop-focused analysis. |
| **Historical Average Delay** | Provides context to the "real-time" number (e.g., "Usually 5m late"). | Medium | Requires joining GTFS-R with static schedules and storing historical data. |
| **Simple Latency Status** | Binary or trinary status (On-time, Delayed, Early) with color coding (Green/Yellow/Red). | Low | Basic UI pattern for quick cognitive processing. |
| **Vehicle Location Map** | Visual confirmation of the data. Users trust the numbers more if they see the dot. | Medium | Uses Leaflet/Mapbox; already partially implemented in current codebase. |

## Differentiators

Features that set this dashboard apart by moving from deterministic "minutes away" to probabilistic reliability.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Delay Probability Distribution (PDF)** | Shows the *likelihood* of arrival within windows, helping users manage risk (e.g., "90% chance it's here by 8:05"). | High | The core "Delay Distribution Dashboard" USP. Requires PDF calculation from histograms. |
| **Time-of-Day/Day-of-Week Sensitivity** | Reliability varies wildly between Monday rush hour and Sunday morning. | Medium | Requires partitioning historical storage (Postgres) by temporal features. |
| **"Worst Case" Buffer Recommendation** | Tells the user exactly how much "buffer time" they should leave to have a 95% chance of catching the bus. | Medium | Derived from the Cumulative Distribution Function (CDF). |
| **Reliability Trend (Last 7 Days)** | Identifies if a stop is getting better or worse (e.g., due to new construction). | Medium | Requires longitudinal historical data. |
| **"Ghost Bus" Indicator** | Reliability is zero if the bus disappears. Tracking telemetry freshness is critical for trust. | Low | Flags buses that haven't sent a GTFS-R update in >3 mins. |

## Anti-Features

Features to explicitly NOT build to maintain focus on the "Reliability Distribution" core value.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Real-time Traffic Rerouting** | High complexity; Google Maps/Transit App already do this better. | Focus on *reliability at the selected stop*, not finding a new route. |
| **Predictive ML (Deep Learning)** | Overkill for initial phase; high infra cost and data requirements. | Use high-resolution historical frequency distributions (empirical PDF). |
| **User Social Reporting** | "Crowdsourced lateness" is noisy and often redundant when GTFS-R is available. | Rely on high-fidelity Translink GTFS-R data for objective ground truth. |
| **Ticketing/Payment Integration** | Massive compliance (PCI) and partnership overhead. | Keep the tool as a pure informational/utility dashboard. |

## Feature Dependencies

```
GTFS-R Ingestion + Schedule Matching → Historical Delay Database (Postgres)
Historical Delay Database → Probabilistic Distribution (PDF/CDF)
Probabilistic Distribution → "Worst Case" Buffer Recommendation
Historical Delay Database → Reliability Trends (Longitudinal)
Telemetry Check → "Ghost Bus" Indicator
```

## MVP Recommendation

Prioritize the "Stop-Focused Reliability" core:
1. **Schedule Join**: Calculating delay by comparing GTFS-R with `stop_times.txt`.
2. **Historical Storage**: Moving observations into TimescaleDB/Postgres partitioned by stop and time window.
3. **Distribution Curve (PDF) Visualization**: A React component showing the lateness histogram for the current/selected time window.
4. **90% Confidence Arrival**: A simple text indicator: "To be safe, be here by [Time]."

Defer: **Multi-stop benchmarking** and **Long-term Trends (>30 days)** to Phase 2 once data density is sufficient.

## Sources

- [Transit App - How late is your bus really?](https://blog.transitapp.com) (UI patterns for historical reliability)
- [Google Maps Commuter Updates](https://blog.google) (Market expectations for delay info)
- [Project Context (.planning/PROJECT.md)](../PROJECT.md) (Internal constraints and tech stack)
