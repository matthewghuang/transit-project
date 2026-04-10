# Architecture

**Analysis Date:** 2026-04-09

## Pattern Overview

**Overall:** Event-driven Microservices with a Real-time Pipeline

**Key Characteristics:**
- **Producer-Consumer:** GTFS realtime data is polled and pushed to Kafka.
- **Data Persistence:** Consumers process Kafka messages, enrich them, and store them in MongoDB with TTL.
- **RESTful API:** A FastAPI service provides access to the persisted vehicle data.
- **Single Page Application:** A React frontend consumes the API to visualize vehicle positions on a map.

## Layers

**Ingestion Layer (Producer):**
- Purpose: Polls external GTFS APIs and publishes updates to Kafka.
- Location: `main.py`
- Contains: HTTP polling logic, Protobuf parsing, and Kafka production.
- Depends on: `google.transit` (GTFS Protobuf), `confluent_kafka`, `requests`.
- Used by: Kafka broker.

**Processing Layer (Consumer):**
- Purpose: Consumes raw vehicle positions from Kafka, enriches them with static GTFS data, and persists them to MongoDB.
- Location: `demo_consumer.py`
- Contains: Kafka consumer loop, CSV-based route enrichment, and MongoDB replacement logic.
- Depends on: `confluent_kafka`, `pymongo`, `pandas`.
- Used by: MongoDB.

**Storage Layer:**
- Purpose: Persists current vehicle positions with a 1-hour TTL.
- Location: `data/` (MongoDB data volume)
- Contains: BSON documents for vehicle updates.
- Depends on: MongoDB.
- Used by: `api.py`.

**Access Layer (API):**
- Purpose: Provides a JSON REST API for the frontend.
- Location: `api.py`
- Contains: FastAPI routes, Pydantic models for validation.
- Depends on: `fastapi`, `pymongo` (AsyncMongoClient).
- Used by: `frontend`.

**Presentation Layer (Frontend):**
- Purpose: Visualizes real-time transit data on a map.
- Location: `frontend/src/`
- Contains: React components, hooks for data fetching, and state management.
- Depends on: `react`, `leaflet`, `zustand`.
- Used by: End users.

## Data Flow

**Real-time Position Flow:**

1. `main.py` polls TransLink GTFS Realtime API every 30 seconds.
2. Changes are detected and published as binary Protobuf messages to Kafka topic `position`.
3. `demo_consumer.py` consumes from `position`, parses Protobuf, and enriches it with route names from `google_transit/routes.txt`.
4. Enriched data is upserted into MongoDB `position.vehicle` collection.
5. `api.py` (FastAPI) fetches all documents from MongoDB and serves them at `/api/vehicles/`.
6. Frontend `usePositions.ts` hook polls the API and updates the Map.

**State Management:**
- **Backend:** Kafka acts as the message buffer; MongoDB holds the current "truth" of vehicle positions.
- **Frontend:** `zustand` (`frontend/src/stores/filterStore.ts`) manages filtering state, while `usePositions.ts` manages the fetched data.

## Key Abstractions

**GTFS Realtime Entities:**
- Purpose: Represents vehicle positions and trip updates in a standardized format.
- Examples: `google.transit.gtfs_realtime_pb2.FeedMessage`
- Pattern: Protocol Buffers (Protobuf).

**Pydantic Models:**
- Purpose: Defines the schema for API responses and ensures type safety between MongoDB and JSON.
- Examples: `VehicleUpdate`, `VehicleDetails`, `Trip`, `Position` in `api.py`.

## Entry Points

**Backend Producer:**
- Location: `main.py`
- Triggers: Scheduled loop (30s sleep).
- Responsibilities: Fetching and broadcasting real-time data.

**Backend Consumer:**
- Location: `demo_consumer.py`
- Triggers: Kafka message arrival.
- Responsibilities: Data enrichment and persistence.

**Web API:**
- Location: `api.py`
- Triggers: HTTP GET requests to `/api/vehicles/`.
- Responsibilities: Serving stored vehicle data.

**Frontend:**
- Location: `frontend/src/index.tsx`
- Triggers: Browser page load.
- Responsibilities: Rendering the dashboard.

## Error Handling

**Strategy:** Fail-soft and retry.

**Patterns:**
- **HTTP Exceptions:** Caught during polling in `main.py` to skip cycles.
- **API Validation:** Pydantic models in `api.py` ensure incoming/outgoing data matches expected structure, returning 422 on failure.
- **Graceful Shutdown:** Consumer handles `KeyboardInterrupt` to close Kafka connections.

## Cross-Cutting Concerns

**Logging:** Basic `print` statements used across Python scripts.
**Validation:** Pydantic on the API layer; Protobuf on the ingestion layer.
**Authentication:** API keys for external GTFS services managed via `.env`.

---

*Architecture analysis: 2026-04-09*
