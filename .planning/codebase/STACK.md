# Technology Stack

**Analysis Date:** 2026-04-09

## Languages

**Primary:**
- Python 3.13 - Backend services (API, producer, consumer)
- TypeScript/JavaScript - Frontend React application

**Secondary:**
- HTML/CSS - Frontend UI
- Shell - Environment scripts

## Runtime

**Environment:**
- Python 3.13
- Node.js (via Parcel for frontend)
- Docker - Containerized infrastructure

**Package Manager:**
- uv - Python package and environment management (lockfile: `uv.lock` present)
- npm - Node.js package management for frontend

## Frameworks

**Core:**
- FastAPI >=0.120.2 - Backend REST API
- React ^19.1.0 - Frontend UI library

**Testing:**
- Not detected (No dedicated test framework configurations like jest or pytest found in exploration)

**Build/Dev:**
- Parcel ^2.16.0 - Frontend bundler and dev server
- Docker Compose - Infrastructure orchestration

## Key Dependencies

**Critical:**
- `confluent-kafka` >=2.12.1 - Kafka integration for realtime data streaming
- `gtfs-realtime-bindings` >=1.0.0 - Protobuf bindings for transit data
- `pymongo` >=4.15.3 - MongoDB driver (including `AsyncMongoClient`)
- `fastapi` - Web framework for `api.py`
- `pandas` - Data processing for GTFS static files in `demo_consumer.py`

**Infrastructure:**
- Kafka (Confluent image) - Message broker
- MongoDB - Primary data store
- Zookeeper - Kafka coordination

## Configuration

**Environment:**
- `.env` files for secrets and service connection strings
- `pyproject.toml` for Python project metadata and dependencies
- `package.json` for frontend configuration

**Build:**
- `Dockerfile` - Backend containerization
- `docker-compose.yml` - Infrastructure definition (Kafka, Mongo, Zookeeper)
- `docker-compose.azure.yaml` - Azure-specific deployment configuration

## Platform Requirements

**Development:**
- Python 3.13
- Node.js
- Docker & Docker Compose

**Production:**
- Cloud-ready via Docker (Azure configuration present in `docker-compose.azure.yaml`)

---

*Stack analysis: 2026-04-09*
