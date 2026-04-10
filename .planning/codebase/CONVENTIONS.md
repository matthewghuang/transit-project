# Coding Conventions

**Analysis Date:** 2026-04-09

## Naming Patterns

**Files:**
- TypeScript/React: PascalCase for components (`Map.tsx`), camelCase for hooks and stores (`usePositions.ts`, `filterStore.ts`).
- Python: snake_case for scripts and modules (`api.py`, `demo_consumer.py`, `main.py`).

**Functions:**
- TypeScript: camelCase for hooks and helpers (`usePositions`), PascalCase for component functions (`App`, `Map`).
- Python: snake_case for functions (`get_all_vehicles`, `map_route_to_name`).

**Variables:**
- TypeScript: camelCase for local variables and constants.
- Python: snake_case for variables, UPPER_SNAKE_CASE for environment variables and global constants (`MONGO_HOST`, `BASE_MODEL_CONFIG`).

**Types:**
- TypeScript: Implicit typing used heavily with React/Zustand; interface/type definitions not explicitly separated in observed files but follow standard TS patterns.
- Python: Pydantic models use PascalCase (`VehicleUpdate`, `Position`).

## Code Style

**Formatting:**
- TypeScript: Indentation uses 2 spaces. Semicolons are used.
- Python: Indentation uses tabs (observed in `api.py` and `demo_consumer.py`).

**Linting:**
- Not explicitly configured in the codebase (no `.eslintrc` or `ruff.toml` found).

## Import Organization

**Order:**
- TypeScript: CSS imports first, then external libraries (React, Zustand), then local components/hooks.
- Python: Standard library imports first, then third-party libraries (pymongo, fastapi, pydantic), then local modules.

**Path Aliases:**
- Not detected. Relative paths are used (e.g., `import { Map } from "./components/Map"`).

## Error Handling

**Patterns:**
- Python (FastAPI): Use of `try/except` blocks with `HTTPException` for API responses. Validation errors are handled automatically by Pydantic.
- TypeScript: React Query handles loading and error states via the `usePositions` hook.

## Logging

**Framework:** `print` statements in Python; `console` for browser logging.

**Patterns:**
- Python: Errors are caught and printed before re-raising as HTTP exceptions.

## Comments

**When to Comment:**
- Python: Docstrings used for FastAPI routes to provide API documentation.
- TypeScript: Minimal inline comments; code is largely self-documenting through naming.

**JSDoc/TSDoc:**
- Not explicitly used in the observed TypeScript files.

## Function Design

**Size:** Small, focused functions (e.g., `get_all_vehicles`, `usePositions`).

**Parameters:** 
- Python: Route handlers typically have no parameters (fetching all) or use Body/Query parameters.
- TypeScript: Hooks return objects containing state and functions.

**Return Values:**
- Python: Pydantic models or lists of models.
- TypeScript: Components return JSX; hooks return state objects.

## Module Design

**Exports:**
- TypeScript: Named exports are preferred (`export function App`).
- Python: Direct function/class definitions in modules meant to be imported or run as scripts.

**Barrel Files:**
- Not detected. Imports target specific files.

---

*Convention analysis: 2026-04-09*
