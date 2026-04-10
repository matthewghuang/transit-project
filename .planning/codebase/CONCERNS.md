# Codebase Concerns

**Analysis Date:** 2026-04-09

## Tech Debt

**Error Handling and Resilience:**
- Issue: Basic `try-except` blocks in `main.py` and `demo_consumer.py` print errors but don't implement robust retry strategies or circuit breakers for external service failures.
- Files: `main.py`, `demo_consumer.py`, `api.py`
- Impact: System may enter failure loops or stop processing without recovery if external APIs or Kafka/MongoDB are temporarily unavailable.
- Fix approach: Implement structured logging and robust retry logic (e.g., using `tenacity` or similar).

**Manual Global State:**
- Issue: Heavy reliance on global variables (`cache`, `first_poll`, `current_data`, `route_id_to_name`) for state management across poll cycles and modules.
- Files: `main.py`, `demo_consumer.py`
- Impact: Makes testing difficult and increases the risk of side effects in more complex flows.
- Fix approach: Encapsulate logic in classes or dependency-injected components.

**Static File Mapping:**
- Issue: Route mapping depends on a static local CSV file `google_transit/routes.txt`.
- Files: `demo_consumer.py`
- Impact: Static files can become outdated; hardcoded paths make deployment more brittle.
- Fix approach: Ingest GTFS static data into the database and join/lookup dynamically.

## Known Bugs

**Empty Message Logic:**
- Issue: In `demo_consumer.py`, the logic for handling empty Kafka messages checks `feed_entity.id` outside of where it is parsed from `msg.value()`, potentially referencing an uninitialized or stale entity ID.
- Files: `demo_consumer.py` (lines 102-107)
- Symptoms: Potential `UnboundLocalError` or deleting the wrong document if an empty message is received after a valid one.
- Trigger: Receiving a message with `msg.value() == None`.
- Workaround: Ensure `feed_entity` is properly scoped or reset within the loop.

## Security Considerations

**API Key Exposure:**
- Issue: The API key is injected directly into URL strings.
- Files: `main.py`
- Risk: While using `os.getenv`, if logs capture the full URL, the API key could be leaked.
- Current mitigation: Uses environment variables via `.env`.
- Recommendations: Use headers for API keys if supported by the provider; ensure URL sanitization in logs.

**Database Authentication:**
- Issue: Default credentials ("root"/"example") are provided as fallbacks in the code.
- Files: `api.py`, `demo_consumer.py`
- Risk: Risk of accidental deployment with default credentials if environment variables are missing.
- Recommendations: Require environment variables in production; remove defaults from source code.

## Performance Bottlenecks

**Full Collection Scan/Transfer:**
- Problem: `/api/vehicles/` fetches all documents from the collection every time.
- Files: `api.py` (line 103), `frontend/src/api/database.ts` (line 40)
- Cause: Lack of filtering or pagination in the API.
- Improvement path: Implement geospatial queries or delta updates to reduce payload size.

**Synchronous Processing in Consumer:**
- Problem: `time.sleep(0.01)` inside the Kafka consumption loop.
- Files: `demo_consumer.py` (line 101)
- Cause: Artificial delay, possibly to avoid overwhelming the DB, but limits throughput.
- Improvement path: Use batch inserts/updates or asynchronous DB drivers.

## Fragile Areas

**Data Serialization/Deserialization:**
- Files: `api.py`, `frontend/src/api/database.ts`
- Why fragile: Tight coupling between the MongoDB document structure and the Pydantic/TypeScript models. Any change in the upstream GTFS-Realtime format or the consumer's transformation logic will break the API and Frontend.
- Safe modification: Implement a versioned API and a mapping layer between DB documents and API responses.
- Test coverage: Gaps in automated testing for data transformation logic.

## Missing Critical Features

**Health Checks & Monitoring:**
- Problem: No health check endpoints or metrics for Kafka consumer lag or API status.
- Blocks: Automated orchestration and alerting in production environments.

## Test Coverage Gaps

**Lack of Automated Tests:**
- What's not tested: Data ingestion logic, API endpoints, and Frontend components.
- Files: Entire codebase (no `tests/` directory or `*.test.*` files found).
- Risk: Regressions are likely when modifying the complex data pipeline.
- Priority: High

---

*Concerns audit: 2026-04-09*
