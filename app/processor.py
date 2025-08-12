import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from .db import engine, Base, SessionLocal
from .models import Event, MinuteAgg
from .config import WINDOW_SECONDS

def ensure_tables():
    Base.metadata.create_all(bind=engine)

def floor_to_minute(dt: datetime) -> datetime:
    return dt.replace(second=0, microsecond=0)

def process_window(db: Session, window_start: datetime, window_end: datetime):
    # aggregate counts and total purchase amount in the window
    rows = (
        db.query(
            Event.action.label("action"),
            func.count(Event.id).label("count"),
            func.sum(Event.amount).label("total_amount"),
        )
        .filter(Event.ts >= window_start, Event.ts < window_end)
        .group_by(Event.action)
        .all()
    )

    for r in rows:
        agg = MinuteAgg(
            minute_start=floor_to_minute(window_start),
            action=r.action,
            count=int(r.count or 0),
            total_amount=float(r.total_amount or 0.0),
        )
        db.add(agg)
    db.commit()

def run_processor():
    ensure_tables()
    print("[processor] starting rolling minute aggregation…")
    last_processed = None
    with SessionLocal() as db:
        while True:
            now = datetime.utcnow()
            if last_processed is None:
                last_processed = now - timedelta(seconds=WINDOW_SECONDS)

            window_start = last_processed
            window_end = window_start + timedelta(seconds=WINDOW_SECONDS)

            if now >= window_end:
                process_window(db, window_start, window_end)
                last_processed = window_end
            else:
                time.sleep(0.5)

if __name__ == "__main__":
    run_processor()
