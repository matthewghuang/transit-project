---
phase: 04-search-first-entry-time-comparisons
verified: 2026-04-10T18:30:00Z
status: human_needed
score: 7/7 must-haves verified
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: 7/7
  gaps_closed:
    - "Stop ID display was missing '#' prefix (from 04-06-PLAN)"
    - "Search was missing stop_code priority (from 04-06-PLAN)"
    - "Hero status was cluttered (from 04-06-PLAN)"
  gaps_remaining: []
  regressions: []
gaps: []
deferred: []
human_verification:
  - test: "Verify that searching for an intersection (e.g. 'Main & 41st') returns correct results in the UI."
    expected: "Results appear in the dropdown as the user types."
    why_human: "Fuzzy search quality and UI responsiveness are best verified by a human user."
  - test: "Verify that selecting a stop from the search results opens the Stop Dashboard and replaces the search UI."
    expected: "Search UI disappears, dashboard shows stop ID and Time Triad."
    why_human: "Core UX transition between landing and dashboard states."
  - test: "Verify that clicking the Time Triad expands it to show the full triad and the reliability chart."
    expected: "The card expands, showing Scheduled/Actual/Predicted times and the PDF chart."
    why_human: "UI interaction and chart visibility (rendering height/layout) verification."
---

# Phase 4: Search-First Entry & Time Comparisons Verification Report

**Phase Goal:** Transition to a search-centric UX that provides immediate value through multi-dimensional arrival times.
**Verified:** 2026-04-10T18:30:00Z
**Status:** human_needed
**Re-verification:** Yes — after gap closure

## Goal Achievement

### Observable Truths

| #   | Truth   | Status     | Evidence       |
| --- | ------- | ---------- | -------------- |
| 1   | Users can find a stop by intersection or 5-digit stop number | ✓ VERIFIED | `api.py` (L213) uses `pg_trgm` and matches `stop_code`/`stop_id`. |
| 2   | The map is removed from the interface | ✓ VERIFIED | Leaflet imports removed from components; `Map.tsx` deleted. |
| 3   | Every search result displays a side-by-side comparison of Scheduled vs. Actual vs. Predicted (Historical) time | ✓ VERIFIED | `TimeTriad.tsx` (L49-56) renders a grid with Scheduled/Actual/Predicted columns. |
| 4   | The search interface is primary and optimized for one-handed mobile use | ✓ VERIFIED | `HeroSearch.tsx` provides a centered, large input search-first landing page. |
| 5   | Searching for a route name (e.g. 'R5') returns stops serving that route | ✓ VERIFIED | `api.py` (L233) logic joins stops with observations to resolve routes. |
| 6   | Actual and Predicted times are null in API if data is unavailable | ✓ VERIFIED | `api.py` provides distinct fields without fallback to scheduled. |
| 7   | Historical delay distribution (PDF) chart is visible in expanded view | ✓ VERIFIED | `TimeTriad.tsx` (L59) renders `DelayDistributionChart` in expanded state. |

**Score:** 7/7 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | ----------- | ------ | ------- |
| `api.py` | Search endpoint & arrival logic | ✓ VERIFIED | Level 1-4. Real data flowing from Postgres. |
| `frontend/src/components/HeroSearch.tsx` | Search landing UI | ✓ VERIFIED | Level 1-4. Wired to `/api/stops/search`. |
| `frontend/src/components/TimeTriad.tsx` | Time triad visualization | ✓ VERIFIED | Level 1-4. Correct Hero logic & expansion. |
| `frontend/src/components/StopDashboard.tsx` | Dashboard container | ✓ VERIFIED | Level 1-4. Wired via `selectedStopId` state. |
| `frontend/src/components/DelayDistributionChart.tsx` | Reliability chart | ✓ VERIFIED | Level 1-4. |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| `HeroSearch.tsx` | `api.py` | `fetch('/api/stops/search')` | ✓ WIRED | Confirmed in code. |
| `api.py` | PostgreSQL | `similarity()` & `stop_code` | ✓ WIRED | Trigram search and ID/Code priority confirmed. |
| `TimeTriad.tsx` | `DelayDistributionChart.tsx` | Props | ✓ WIRED | Conditional rendering confirmed. |
| `App.tsx` | `StopDashboard.tsx` | `selectedStopId` | ✓ WIRED | View switching logic confirmed. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `TimeTriad.tsx` | `data` | `api.py` -> DB | ✓ FLOWING | Fetches actual/predicted times from DB. |
| `HeroSearch.tsx` | `results` | `api.py` -> `stops` table | ✓ FLOWING | Returns real stop metadata. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Stop Search API | `curl .../api/stops/search?q=Main` | JSON results | ✓ PASS |
| ID Prioritization | `curl .../api/stops/search?q=50959` | First result is 50959 | ✓ PASS |
| Map removal | `grep -r "leaflet" frontend/src` | No JS/TS usage found | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| SRCH-01 | 04-02 | Search by intersection | ✓ SATISFIED | Trigram search in `api.py`. |
| SRCH-02 | 04-01 | Search by stop number | ✓ SATISFIED | `stop_code` matching in `api.py`. |
| SRCH-03 | 04-01 | Backend fuzzy matching | ✓ SATISFIED | `pg_trgm` used on `stop_name`. |
| SRCH-04 | 04-03 | Triad time display | ✓ SATISFIED | `TimeTriad.tsx` implements triad. |
| SRCH-05 | 04-02 | Mobile search UI | ✓ SATISFIED | `HeroSearch.tsx` centered layout. |
| UIO-01 | 04-02 | Map removal | ✓ SATISFIED | Component and logic removed. |
| UIO-04 | 04-03 | Expanded triad detail | ✓ SATISFIED | `TimeTriad.tsx` expansion logic. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `frontend/src/index.html` | 13 | Leaflet CSS link | ℹ️ INFO | Leftover CSS link; no functional impact. |

### Human Verification Required

### 1. Search UX & Result Quality

**Test:** Perform searches for specific stop codes (e.g. 50959) and intersections (e.g. "Main & 41st").
**Expected:** Results appear instantly. Exact ID matches are prioritized. Names are fuzzy-matched correctly.
**Why human:** Evaluating the subjective quality and responsiveness of search results.

### 2. View Transition Flow

**Test:** Select a stop result from the search bar.
**Expected:** The hero landing page is replaced by the stop dashboard without a full page reload.
**Why human:** Verifying the smoothness of the SPA state transition.

### 3. Time Triad & Chart Visibility

**Test:** In the dashboard, click the "Hero Time" card to expand it.
**Expected:** The card expands to show Scheduled/Actual/Predicted times in a grid, and the delay distribution chart renders below them.
**Why human:** Verifying layout stability and chart rendering quality.

### Gaps Summary

Phase 4 is technically complete. All UAT gaps identified in previous plans (04-04 and 04-06) regarding stop ID display, search priority, and UI centering have been resolved in the code. The transition from map-centric to search-centric is successful.

---

_Verified: 2026-04-10T18:30:00Z_
_Verifier: the agent (gsd-verifier)_
