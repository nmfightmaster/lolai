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
