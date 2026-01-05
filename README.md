# AI League Coach (Step 1)

Minimal Riot API connectivity setup.

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Bash/Zsh
   # source .venv/bin/activate.fish # Fish
   pip install -r requirements.txt
   ```

2. **Environment**:
   Copy `.env.example` to `.env` and set your `RIOT_API_KEY`.
   ```bash
   cp .env.example .env
   ```

## Usage

### Smoke Test
Verify connectivity by fetching a match. You need a valid Match ID (e.g., from [op.gg](https://op.gg) `NA1_...`).
```bash
python smoke_test.py <MATCH_ID>
```
Example:
```bash
python smoke_test.py NA1_5001765063
```
This will save `match_<ID>.json` and `timeline_<ID>.json` to `data/`.

### Testing
Run unit tests:
```bash
pytest
```
