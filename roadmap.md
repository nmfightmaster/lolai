# Project Roadmap: AI League of Legends Coach

## Overview
Building an AI-assisted coaching app using Riot's API.
**Philosophy**: Incremental, testable steps. Boring tech until necessary.

## Phase 1: Foundation (Current)
- [x] **Step 1: Connectivity & Infrastructure**
    - Established Python + Httpx + Pydantic stack.
    - Setup minimal CI and testing.
    - Validated connectivity with Smoke Test.

- [ ] **Step 2: Data Acquisition (Match History)**
    - Implement `get_match_history(puuid)` with pagination.
    - Bulk fetch logic (rate limit handling).
    - CLI tool to "fetch last N matches for User X".

- [ ] **Step 3: Data Parsing & Storage**
    - Define domain models for "Game Stats" (simpler than raw Riot JSON).
    - Parse raw Timeline data into events (Kills, Objectives, Gold diffs).
    - Decide on Database vs continuing with File persistence (SQLite likely).

## Phase 2: Analysis Engine
- [ ] **Step 4: Rule-Based Analysis**
    - Implement non-AI logic: "CS per minute", "Objective participation".
    - Compare user stats vs "Average" (requires fetching Challenger data?).

- [ ] **Step 5: LLM Context Integration**
    - Generate text summaries of a match.
    - Create prompt templates: "Given this timeline, why did I lose?"
    - Connect to OpenAI/Gemini API.

## Phase 3: Productization
- [ ] **Step 6: User Interface**
    - Simple Web UI (FastAPI + Jinja or React).
    - Visual timeline graph.

- [ ] **Step 7: Live Assistance (Optional)**
    - Real-time client via LCU (League Client Update) API.
