# External Integrations

**Analysis Date:** 2026-04-09

## APIs & External Services

**Transit Data:**
- TransLink GTFS Realtime API - Source of vehicle positions and realtime updates
  - SDK/Client: `requests` + `gtfs-realtime-bindings`
  - Auth: `API_KEY` (stored in `.env`)
  - Endpoints: `https://gtfsapi.translink.ca/v3/gtfsrealtime` and `https://gtfsapi.translink.ca/v3/gtfsposition`

## Data Storage

**Databases:**
- MongoDB
  - Connection: `MONGO_CONNECTION_STRING` or individual `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_HOST`, `MONGO_PORT` vars
  - Client: `pymongo` (Synchronous in consumer, `AsyncMongoClient` in API)
  - Usage: Storing current vehicle positions with TTL indices for automatic cleanup

**Message Broker:**
- Apache Kafka
  - Connection: `KAFKA_BOOTSTRAP_SERVERS`
  - Client: `confluent-kafka`
  - Usage: Streaming vehicle position updates from producer (`main.py`) to consumer (`demo_consumer.py`)

## Authentication & Identity

**Auth Provider:**
- Custom / API Key
  - Implementation: API Key required for TransLink API access. MongoDB uses root credentials defined in environment variables.

## Monitoring & Observability

**Error Tracking:**
- None detected (Basic console logging in Python scripts)

**Logs:**
- Standard output (captured by Docker/Console)

## CI/CD & Deployment

**Hosting:**
- Azure (Inferred from `docker-compose.azure.yaml`)

**CI Pipeline:**
- Not detected

## Environment Configuration

**Required env vars:**
- `API_KEY` - TransLink API authentication
- `MONGO_USER`, `MONGO_PASSWORD` - MongoDB credentials
- `KAFKA_BOOTSTRAP_SERVERS` - Kafka connection point
- `MONGO_CONNECTION_STRING` - Optional full MongoDB URI

**Secrets location:**
- `.env` and `.env.influxdb2-*` files (Local)

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

---

*Integration audit: 2026-04-09*
