# Implementation History

This file logs key architectural decisions and completed milestones. Use this to orient yourself in a new agent session.

## 2026-01-05: Step 1 - Connectivity & Foundation
**Context**: Initial project setup.
**Changes**:
- **Stack**: Chosen Python 3.10+ (for future AI eco), `httpx` (async ready), `pydantic` (validation), `pytest`.
- **Structure**: `src/` module pattern, `data/` for flat-file persistence.
- **Infrastructure**: Added Github Actions (CI), `ruff` linting, `.env` management.
- **Key Decisions**:
    - *Storage*: Kept to flat JSON files for MVP. No DB yet.
    - *Riot Client*: Thin wrapper around `httpx`. Manual method definition over generic wrapper for type safety.
    - *Validation*: Basic Pydantic models with `extra='ignore'` to enable forward compatibility with Riot API changes.

**Current State**:
- Logic: `src.riot.RiotClient` can fetch match & timeline.
- Validation: `src.schemas` has base DTOs.
- Test: `smoke_test.py` proves end-to-end connectivity.

## 2026-01-05: Step 2 - Data Acquisition (Match History)
**Context**: Need to fetch user history to build a dataset for analysis.
**Changes**:
- **API**: Added `get_match_ids_by_puuid` to `RiotClient`. Added basic rate limit handling (429 retry-after sleep).
- **Tools**: Created `fetch_history.py` CLI for bulk fetching.
- **Workflow**: Script checks local existence before fetching to save API calls.
- **Testing**: Added `tests/test_riot_history.py` to mock and verify pagination/filtering logic.

**Current State**:
- Can fetch N matches for a user via CLI.
- Data saved to `data/` as `match_{id}.json` and `timeline_{id}.json`.

## 2026-01-05: Step 3 - Data Parsing & Storage
**Context**: Need structured data for analysis, raw JSON is too deep/complex.
**Changes**:
- **Models**: Defined `GameStatsDto` and `TimelineEventDto` pydantic models.
- **DB**: Added `sqlite3` persistence with `src/database.py`.
- **Parsing**: Implemented translation layer in `src/parsing.py` to flatten Riot JSON.
- **Process**: Created `src/process.py` to ingest existing JSON files into DB.

**Current State**:
- `lolai.db` contains parsed stats and events.
- Unit tests cover parsing and DB operations.

## 2026-01-05: Step 4 - Rule-Based Analysis
**Context**: Implement basic aggregation and comparison logic for player stats.
**Changes**:
- **Logic**: Created `src/analysis.py` with `AnalysisEngine` class.
- **DB**: Added `get_recent_games` to `src/database.py`.
- **CLI**: Added `analyze.py` to run reports via CLI. Support for `GameName#Tag` and direct `PUUID`.
- **Testing**: Added `tests/test_analysis.py` for calculation verification.

**Current State**:
- Can analyze last N games for a user.
- Reports Win Rate, KDA, CSPM, Vision Score, and Gold/Min.
- Compares against static baseline (Gold/Plat average).

