# Architecture Research: Dynamic Confidence & Arrive-By Times

**Domain:** Real-time Transit Analytics
**Researched:** April 10, 2026
**Confidence:** HIGH

## Standard Architecture

### System Overview

Focusing strictly on the v1.2 additions (Dynamic Confidence Slider & Dynamic Percentile API) interacting with the existing v1.0 pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │ConfidenceSlider│  │  filterStore   │  │  usePositions  │ │
│  │  (New UI Comp) │  │  (Zustand)     │  │  (Data Fetch)  │ │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘ │
│          │                   │                   │          │
│          └──────(updates)────┘                   │          │
│                              │                   │          │
│                              └─────(triggers)────┘          │
├───────────────────────────────────────┬─────────────────────┤
│                                       │ ?confidence=0.85    │
├───────────────────────────────────────▼─────────────────────┤
│                      Backend (FastAPI)                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    api.py Endpoint                  │    │
│  │     (Dynamic Percentile & Safe Arrive-By Logic)     │    │
│  └──────────────────────────┬──────────────────────────┘    │
├─────────────────────────────┼───────────────────────────────┤
│                             │ SQL: percentile_cont(val)     │
├─────────────────────────────▼───────────────────────────────┤
│                     Database (TimescaleDB)                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Historical Delays Table             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| `ConfidenceSlider` | Capture user's desired reliability threshold (e.g., 50%-99%). | React component (HTML input `type="range"` or a library component). |
| `filterStore` | Manage global state for the selected confidence level. | Zustand slice inside `frontend/src/stores/filterStore.ts`. |
| `usePositions` (or new hook) | Fetch data from API with the new confidence parameter. | React Query / Fetch wrapper reacting to store changes. |
| `api.py` Routes | Parse the `confidence` query parameter, orchestrate the DB query, and enforce the "never later than scheduled" rule. | FastAPI `@app.get` route with `Query` validation. |
| TimescaleDB Query | Compute the exact percentile of historical delays dynamically. | PostgreSQL `percentile_cont()` aggregation function. |

## Recommended Project Structure

```
frontend/src/
├── components/
│   ├── controls/
│   │   └── ConfidenceSlider.tsx    # NEW: UI component for threshold selection
│   └── map/
│       └── ...                     # Existing UI components consuming the new predictions
├── stores/
│   └── filterStore.ts              # MODIFIED: Include `confidenceLevel` state
└── hooks/
    └── usePositions.ts             # MODIFIED: Pass `confidence` query param to API

backend/
└── api.py                          # MODIFIED: API endpoints and Pydantic schemas
```

### Structure Rationale

- **`frontend/src/components/controls/`:** Isolates the new interactive control from the complex map logic.
- **`backend/api.py`:** Since the backend is lightweight, expanding the existing endpoints (rather than creating a new service) keeps the architecture cohesive.

## Architectural Patterns

### Pattern 1: Dynamic Percentile Pushdown

**What:** Pushing the percentile calculation down to the database layer rather than fetching all raw observations and calculating in memory.
**When to use:** When the dataset is large (like historical transit delays) and moving data across the network is slow.
**Trade-offs:** Increases database CPU load but significantly reduces memory usage and network latency for the backend service.

**Example:**
```sql
SELECT 
  route_id, 
  percentile_cont($1) WITHIN GROUP (ORDER BY delay_seconds) as predicted_delay
FROM historical_delays
WHERE stop_id = $2
GROUP BY route_id;
```

### Pattern 2: Debounced State Synchronization

**What:** The slider updates local component state immediately for smooth UI, but debounces updates to the global `filterStore` (which triggers API calls).
**When to use:** For continuous input controls (sliders) that trigger expensive network/database operations.
**Trade-offs:** Slight delay between user stopping the slider and data updating, but prevents API spam and DB overload.

## Data Flow

### Request Flow (Confidence Change)

```
[User drags slider to 90%]
    ↓
[ConfidenceSlider] → (debounces 300ms) → [filterStore (Zustand)]
    ↓
[usePositions (Hook)] detects store change, triggers fetch: GET /api/vehicles/?confidence=0.9
    ↓
[FastAPI Route] validates input (0.5 <= conf <= 0.99)
    ↓
[TimescaleDB] executes query using `percentile_cont(0.9)`
    ↓
[FastAPI Route] shapes response, applies "predicted <= scheduled" constraint
    ↓
[Frontend] renders updated area chart and conservative arrive-by times
```

### Key Data Flows

1. **Arrive-by Time Calculation Flow:** 
   - The database computes the delay `D` at the given percentile. 
   - The backend applies the logic: `predicted_arrival = scheduled_arrival + D`. 
   - The backend MUST enforce the constraint `predicted_arrival <= scheduled_arrival` if `D < 0` (bus historically runs early), ensuring commuters never miss early buses. This value is then passed to the frontend.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| Current | On-the-fly `percentile_cont()` is sufficient for current traffic and data volume. |
| High read volume | Introduce materialized views (TimescaleDB Continuous Aggregates) for standard confidence intervals (e.g., 50%, 75%, 90%, 95%) and snap the UI slider to those specific discrete steps. |

### Scaling Priorities

1. **First bottleneck:** TimescaleDB CPU utilization spiking due to `percentile_cont` over massive unaggregated historical rows. *Fix: Restrict the time window (e.g., "last 30 days") or implement continuous aggregates.*
2. **Second bottleneck:** API thrashing from fast slider movements. *Fix: Stricter debouncing on the frontend, and potential request cancellation (AbortController) in the fetch hook.*

## Anti-Patterns

### Anti-Pattern 1: In-Memory Percentile Calculation

**What people do:** Fetch all raw historical delay rows for a stop into the FastAPI memory and use standard libraries to calculate the percentile.
**Why it's wrong:** As the historical dataset grows, moving thousands of rows across the network and loading them into Python memory for every single user request will crash the backend.
**Do this instead:** Push the calculation down to TimescaleDB using `percentile_cont()`.

### Anti-Pattern 2: Trusting Client-Side Constraints

**What people do:** Calculating the "conservative arrive-by time" directly in the React frontend based on raw distribution data.
**Why it's wrong:** Fragments business logic. Different clients (or future integrations) might calculate it differently, leading to missed buses.
**Do this instead:** Enforce the "never later than scheduled" logic inside the FastAPI backend.

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Frontend ↔ Backend | REST API (GET) | Add `?confidence=0.85` query parameter to existing delay/position endpoints. Return schema updated to include the definitive `conservative_arrive_by` timestamp. |
| Backend ↔ TimescaleDB | Async SQL | Ensure proper indexing on `(stop_id, route_id, time_of_day)` to support the on-the-fly `percentile_cont` calculations without full table scans. |

## Suggested Build Order

To minimize friction and ensure stable integration, build from the data layer up:

1. **Backend & Database (`api.py`)**
   - Add the `confidence` query parameter to the FastAPI endpoint (defaulting to e.g., 0.85).
   - Update the TimescaleDB SQL queries to use `percentile_cont()` dynamically.
   - Implement the "never later than scheduled" logic overhaul in the backend.
2. **Frontend State (`filterStore.ts` & Hooks)**
   - Add `confidenceLevel` to the Zustand store.
   - Update the API fetching hooks to append the new query parameter.
3. **Frontend UI (`ConfidenceSlider.tsx`)**
   - Build the interactive slider component with debouncing.
   - Update the UI to prominently display the conservative arrive-by time and reflect the chosen confidence interval on the visualization.

## Sources

- `.planning/PROJECT.md` (Milestone v1.2 specifications)
- PostgreSQL Documentation (`percentile_cont` aggregate function)

---
*Architecture research for: Dynamic Confidence & Arrive-By Times (v1.2)*
*Researched: April 10, 2026*