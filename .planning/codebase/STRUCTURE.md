# Codebase Structure

**Analysis Date:** 2026-04-09

## Directory Layout

```
transit-data/
├── google_transit/      # Static GTFS data files (CSV)
├── frontend/            # React + TypeScript frontend application
│   ├── src/
│   │   ├── api/         # Frontend API clients
│   │   ├── components/  # React components (Map, Table)
│   │   ├── hooks/       # Custom React hooks (Data fetching)
│   │   ├── stores/      # State management (Zustand)
│   │   └── index.tsx    # Frontend entry point
├── data/                # MongoDB data persistence volume
├── api.py               # FastAPI backend server
├── main.py              # Kafka producer (GTFS Poller)
├── demo_consumer.py     # Kafka consumer (Enrichment & Storage)
├── docker-compose.yml   # Infrastructure orchestration
└── pyproject.toml       # Python dependencies and configuration
```

## Directory Purposes

**google_transit/:**
- Purpose: Contains static transit data used for enriching real-time feeds.
- Contains: CSV files following the GTFS standard.
- Key files: `routes.txt`, `stops.txt`, `trips.txt`.

**frontend/src/:**
- Purpose: Source code for the dashboard user interface.
- Contains: TSX components, styles, and logic.
- Key files: `App.tsx`, `components/Map.tsx`.

**data/:**
- Purpose: Local storage for MongoDB database files.
- Contains: WiredTiger storage engine files and diagnostic data.
- Generated: Yes (by MongoDB).

## Key File Locations

**Entry Points:**
- `main.py`: The starting point for the data ingestion pipeline.
- `api.py`: The starting point for the web service.
- `frontend/src/index.tsx`: The starting point for the client-side app.

**Configuration:**
- `docker-compose.yml`: Defines the Kafka, MongoDB, and Zookeeper infrastructure.
- `.env`: (Ignored/Not read) Contains API keys and connection strings.
- `pyproject.toml`: Defines Python project metadata and dependencies.

**Core Logic:**
- `demo_consumer.py`: Handles the transformation from Protobuf to MongoDB documents.
- `frontend/src/hooks/usePositions.ts`: Manages the lifecycle of fetching and updating vehicle positions in the UI.

**Testing:**
- Not detected (No dedicated `tests/` directory found in root).

## Naming Conventions

**Files:**
- Python: `snake_case.py` (e.g., `demo_consumer.py`).
- TypeScript/React: `PascalCase.tsx` for components (e.g., `FilterTable.tsx`), `camelCase.ts` for logic (e.g., `usePositions.ts`).

**Directories:**
- General: `lowercase` (e.g., `frontend`, `google_transit`).

## Where to Add New Code

**New Feature (Data Processing):**
- Primary code: Create a new consumer script or modify `demo_consumer.py`.
- Infrastructure: Update `docker-compose.yml` if new services are needed.

**New API Endpoint:**
- Implementation: `api.py`.
- Model: Add new Pydantic classes in `api.py`.

**New Frontend Component:**
- Implementation: `frontend/src/components/`.
- Styling: `frontend/src/App.css` or component-specific CSS.

**Utilities:**
- Python: Create a `utils/` directory or add to existing scripts if small.
- Frontend: `frontend/src/hooks/` for logic-related helpers.

## Special Directories

**data/:**
- Purpose: MongoDB persistent storage.
- Generated: Yes
- Committed: No (usually gitignored, though listed in exploration).

**frontend/node_modules/:**
- Purpose: Frontend dependencies.
- Generated: Yes (by npm/yarn).
- Committed: No.

---

*Structure analysis: 2026-04-09*
