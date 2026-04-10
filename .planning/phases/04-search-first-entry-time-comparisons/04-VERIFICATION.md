---
phase: 04-search-first-entry-time-comparisons
verified: 2026-04-10T18:15:00Z
status: human_needed
score: 7/7 must-haves verified
overrides_applied: 0
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
**Verified:** 2026-04-10T18:15:00Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| #   | Truth   | Status     | Evidence       |
| --- | ------- | ---------- | -------------- |
| 1   | Users can find a stop by intersection or 5-digit stop number | ✓ VERIFIED | `api.py` implements fuzzy search and stop_id prioritization; `HeroSearch.tsx` provides the UI. |
| 2   | The map is removed from the interface | ✓ VERIFIED | `Leaflet` imports removed; `Map.tsx` deleted; `App.tsx` no longer uses Map. |
| 3   | Every search result displays a side-by-side comparison of Scheduled vs. Actual vs. Predicted (Historical) time | ✓ VERIFIED | `TimeTriad.tsx` implements the triad display with fallback logic. |
| 4   | The search interface is primary and optimized for one-handed mobile use | ✓ VERIFIED | `HeroSearch.tsx` provides a centered, large input search-first landing page. |
| 5   | Searching for a route name (e.g. 'R5') returns stops serving that route | ✓ VERIFIED | `api.py` contains logic to resolve route names and JOIN with observations. |
| 6   | Actual and Predicted times are null in API if data is unavailable | ✓ VERIFIED | `api.py` removed fallbacks to scheduled time. |
| 7   | Historical delay distribution (PDF) chart is visible in expanded view | ✓ VERIFIED | `TimeTriad.tsx` renders `DelayDistributionChart` in expanded state with min-height. |

**Score:** 7/7 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | ----------- | ------ | ------- |
| `api.py` | Search endpoint & arrival logic | ✓ VERIFIED | Level 1-3 passed. |
| `frontend/src/components/HeroSearch.tsx` | Search landing UI | ✓ VERIFIED | Level 1-3 passed. Centered search bar + dropdown. |
| `frontend/src/components/TimeTriad.tsx` | Time triad visualization | ✓ VERIFIED | Level 1-3 passed. Implements Hero Time logic. |
| `frontend/src/components/StopDashboard.tsx` | Dashboard container | ✓ VERIFIED | Level 1-3 passed. Simplified UI. |
| `frontend/src/components/DelayDistributionChart.tsx` | Reliability chart | ✓ VERIFIED | Level 1-3 passed. |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| `/api/stops/search` | PostgreSQL `stops` table | trigram search | ✓ WIRED | `pg_trgm` extension used with GIST index. |
| `HeroSearch.tsx` | `/api/stops/search` | `ky` fetch | ✓ WIRED | Implements auto-suggest logic. |
| `App.tsx` | `StopDashboard.tsx` | `selectedStopId` state | ✓ WIRED | Switches views based on selection. |
| `TimeTriad.tsx` | `DelayDistributionChart.tsx` | React Component | ✓ WIRED | Conditional rendering in expanded state. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `TimeTriad.tsx` | `data` | `useNextBuses` -> API | ✓ FLOWING | Fetches real-time and historical data from DB. |
| `HeroSearch.tsx` | `results` | `/api/stops/search` | ✓ FLOWING | Uses trigram search on `stops` table. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Stop Search API | `curl .../api/stops/search?q=Main` | JSON results | ✓ PASS |
| ID Prioritization | `curl .../api/stops/search?q=50959` | First result is 50959 | ✓ PASS |
| Map removal | `grep -r "leaflet" frontend/src` | No JS/TS usage found | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| SRCH-01 | 04-02 | Search by intersection | ✓ SATISFIED | `HeroSearch.tsx` + `api.py` fuzzy search. |
| SRCH-02 | 04-01 | Search by stop number | ✓ SATISFIED | `api.py` prioritizes numeric stop_id. |
| SRCH-03 | 04-01 | Backend fuzzy matching | ✓ SATISFIED | `pg_trgm` extension enabled in `db_init.py`. |
| SRCH-04 | 04-03 | Triad time display | ✓ SATISFIED | `TimeTriad.tsx` displays triad. |
| SRCH-05 | 04-02 | Mobile search UI | ✓ SATISFIED | `HeroSearch.tsx` design. |
| UIO-01 | 04-02 | Map removal | ✓ SATISFIED | `Map.tsx` deleted. |
| UIO-04 | 04-03 | Expanded triad detail | ✓ SATISFIED | `TimeTriad.tsx` expansion logic. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `frontend/src/index.html` | 13 | Leaflet CSS link | ℹ️ INFO | Leftover CSS link in HTML; doesn't affect functionality. |

### Human Verification Required

### 1. Search Interaction & Accuracy

**Test:** Type common intersection names and stop IDs in the search bar.
**Expected:** Dropdown appears quickly with relevant suggestions. Numeric searches put the exact match at the top.
**Why human:** Evaluating the "feel" and accuracy of fuzzy search results.

### 2. View Transition

**Test:** Select a stop from the search results.
**Expected:** The search UI is replaced by the stop dashboard.
**Why human:** Verifying the smoothness of the SPA navigation flow.

### 3. Time Triad Expansion & Chart

**Test:** Click on the "Next Arrival" time triad card.
**Expected:** Card expands to show all three times and the delay distribution chart. Chart is clearly visible and readable.
**Why human:** Layout and visualization quality verification.

### Gaps Summary

No technical gaps found. The implementation matches the goal of a search-first, map-free dashboard with multi-dimensional arrival times. The code is well-wired, and the backend supports the required search and analytical queries.

---

_Verified: 2026-04-10T18:15:00Z_
_Verifier: the agent (gsd-verifier)_