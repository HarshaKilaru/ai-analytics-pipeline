from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "events.db"

# Event generation rate (events/sec)
EVENTS_PER_SEC = 4

# Aggregation window size in seconds
WINDOW_SECONDS = 60
