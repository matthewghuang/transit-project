<!-- GSD:project-start source:PROJECT.md -->
## Project

**Translink Delay Distribution Dashboard**

A real-time transit dashboard that visualizes the reliability of bus routes at specific stops. Instead of just showing "minutes away," it provides a probability density visualization of how late a bus is likely to be based on historical performance for that specific time of day.

**Core Value:** Empower commuters with probabilistic insights into bus reliability, allowing for better-informed travel decisions beyond simple real-time estimates.

### Constraints

- **Tech Stack**: Python (FastAPI, Confluent Kafka), PostgreSQL (TimescaleDB preferred), React.
- **Data Freshness**: GTFS-R polled every 30 seconds (Translink API limit/preference).
- **Storage**: `stop_times.txt` is ~90MB; historical delay observations will grow significantly over time.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.13 - Backend services (API, producer, consumer)
- TypeScript/JavaScript - Frontend React application
- HTML/CSS - Frontend UI
- Shell - Environment scripts
## Runtime
- Python 3.13
- Node.js (via Parcel for frontend)
- Docker - Containerized infrastructure
- uv - Python package and environment management (lockfile: `uv.lock` present)
- npm - Node.js package management for frontend
## Frameworks
- FastAPI >=0.120.2 - Backend REST API
- React ^19.1.0 - Frontend UI library
- Not detected (No dedicated test framework configurations like jest or pytest found in exploration)
- Parcel ^2.16.0 - Frontend bundler and dev server
- Docker Compose - Infrastructure orchestration
## Key Dependencies
- `confluent-kafka` >=2.12.1 - Kafka integration for realtime data streaming
- `gtfs-realtime-bindings` >=1.0.0 - Protobuf bindings for transit data
- `pymongo` >=4.15.3 - MongoDB driver (including `AsyncMongoClient`)
- `fastapi` - Web framework for `api.py`
- `pandas` - Data processing for GTFS static files in `demo_consumer.py`
- Kafka (Confluent image) - Message broker
- MongoDB - Primary data store
- Zookeeper - Kafka coordination
## Configuration
- `.env` files for secrets and service connection strings
- `pyproject.toml` for Python project metadata and dependencies
- `package.json` for frontend configuration
- `Dockerfile` - Backend containerization
- `docker-compose.yml` - Infrastructure definition (Kafka, Mongo, Zookeeper)
- `docker-compose.azure.yaml` - Azure-specific deployment configuration
## Platform Requirements
- Python 3.13
- Node.js
- Docker & Docker Compose
- Cloud-ready via Docker (Azure configuration present in `docker-compose.azure.yaml`)
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- TypeScript/React: PascalCase for components (`Map.tsx`), camelCase for hooks and stores (`usePositions.ts`, `filterStore.ts`).
- Python: snake_case for scripts and modules (`api.py`, `demo_consumer.py`, `main.py`).
- TypeScript: camelCase for hooks and helpers (`usePositions`), PascalCase for component functions (`App`, `Map`).
- Python: snake_case for functions (`get_all_vehicles`, `map_route_to_name`).
- TypeScript: camelCase for local variables and constants.
- Python: snake_case for variables, UPPER_SNAKE_CASE for environment variables and global constants (`MONGO_HOST`, `BASE_MODEL_CONFIG`).
- TypeScript: Implicit typing used heavily with React/Zustand; interface/type definitions not explicitly separated in observed files but follow standard TS patterns.
- Python: Pydantic models use PascalCase (`VehicleUpdate`, `Position`).
## Code Style
- TypeScript: Indentation uses 2 spaces. Semicolons are used.
- Python: Indentation uses tabs (observed in `api.py` and `demo_consumer.py`).
- Not explicitly configured in the codebase (no `.eslintrc` or `ruff.toml` found).
## Import Organization
- TypeScript: CSS imports first, then external libraries (React, Zustand), then local components/hooks.
- Python: Standard library imports first, then third-party libraries (pymongo, fastapi, pydantic), then local modules.
- Not detected. Relative paths are used (e.g., `import { Map } from "./components/Map"`).
## Error Handling
- Python (FastAPI): Use of `try/except` blocks with `HTTPException` for API responses. Validation errors are handled automatically by Pydantic.
- TypeScript: React Query handles loading and error states via the `usePositions` hook.
## Logging
- Python: Errors are caught and printed before re-raising as HTTP exceptions.
## Comments
- Python: Docstrings used for FastAPI routes to provide API documentation.
- TypeScript: Minimal inline comments; code is largely self-documenting through naming.
- Not explicitly used in the observed TypeScript files.
## Function Design
- Python: Route handlers typically have no parameters (fetching all) or use Body/Query parameters.
- TypeScript: Hooks return objects containing state and functions.
- Python: Pydantic models or lists of models.
- TypeScript: Components return JSX; hooks return state objects.
## Module Design
- TypeScript: Named exports are preferred (`export function App`).
- Python: Direct function/class definitions in modules meant to be imported or run as scripts.
- Not detected. Imports target specific files.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- **Producer-Consumer:** GTFS realtime data is polled and pushed to Kafka.
- **Data Persistence:** Consumers process Kafka messages, enrich them, and store them in MongoDB with TTL.
- **RESTful API:** A FastAPI service provides access to the persisted vehicle data.
- **Single Page Application:** A React frontend consumes the API to visualize vehicle positions on a map.
## Layers
- Purpose: Polls external GTFS APIs and publishes updates to Kafka.
- Location: `main.py`
- Contains: HTTP polling logic, Protobuf parsing, and Kafka production.
- Depends on: `google.transit` (GTFS Protobuf), `confluent_kafka`, `requests`.
- Used by: Kafka broker.
- Purpose: Consumes raw vehicle positions from Kafka, enriches them with static GTFS data, and persists them to MongoDB.
- Location: `demo_consumer.py`
- Contains: Kafka consumer loop, CSV-based route enrichment, and MongoDB replacement logic.
- Depends on: `confluent_kafka`, `pymongo`, `pandas`.
- Used by: MongoDB.
- Purpose: Persists current vehicle positions with a 1-hour TTL.
- Location: `data/` (MongoDB data volume)
- Contains: BSON documents for vehicle updates.
- Depends on: MongoDB.
- Used by: `api.py`.
- Purpose: Provides a JSON REST API for the frontend.
- Location: `api.py`
- Contains: FastAPI routes, Pydantic models for validation.
- Depends on: `fastapi`, `pymongo` (AsyncMongoClient).
- Used by: `frontend`.
- Purpose: Visualizes real-time transit data on a map.
- Location: `frontend/src/`
- Contains: React components, hooks for data fetching, and state management.
- Depends on: `react`, `leaflet`, `zustand`.
- Used by: End users.
## Data Flow
- **Backend:** Kafka acts as the message buffer; MongoDB holds the current "truth" of vehicle positions.
- **Frontend:** `zustand` (`frontend/src/stores/filterStore.ts`) manages filtering state, while `usePositions.ts` manages the fetched data.
## Key Abstractions
- Purpose: Represents vehicle positions and trip updates in a standardized format.
- Examples: `google.transit.gtfs_realtime_pb2.FeedMessage`
- Pattern: Protocol Buffers (Protobuf).
- Purpose: Defines the schema for API responses and ensures type safety between MongoDB and JSON.
- Examples: `VehicleUpdate`, `VehicleDetails`, `Trip`, `Position` in `api.py`.
## Entry Points
- Location: `main.py`
- Triggers: Scheduled loop (30s sleep).
- Responsibilities: Fetching and broadcasting real-time data.
- Location: `demo_consumer.py`
- Triggers: Kafka message arrival.
- Responsibilities: Data enrichment and persistence.
- Location: `api.py`
- Triggers: HTTP GET requests to `/api/vehicles/`.
- Responsibilities: Serving stored vehicle data.
- Location: `frontend/src/index.tsx`
- Triggers: Browser page load.
- Responsibilities: Rendering the dashboard.
## Error Handling
- **HTTP Exceptions:** Caught during polling in `main.py` to skip cycles.
- **API Validation:** Pydantic models in `api.py` ensure incoming/outgoing data matches expected structure, returning 422 on failure.
- **Graceful Shutdown:** Consumer handles `KeyboardInterrupt` to close Kafka connections.
## Cross-Cutting Concerns
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
