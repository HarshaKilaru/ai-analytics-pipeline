# AI‑Augmented Analytics Pipeline (Local MVP)

Minimal end‑to‑end pipeline:
- **Ingest:** simulate events (view/click/purchase) into SQLite
- **Process:** rolling 1‑minute aggregates
- **Serve:** FastAPI endpoints for metrics + a simple “AI‑style” insight

## Architecture
Ingest → SQLite → Processor (minute aggregates) → FastAPI → JSON/Insights

## How to Run (Windows, CMD)

```cmd
.\.venv\Scripts\activate
pip install -r requirements.txt
run.bat
