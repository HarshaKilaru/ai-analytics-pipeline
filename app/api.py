from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from .db import get_db, engine, Base
from .models import MinuteAgg
from .llm import generate_insight

app = FastAPI(title="AI-Augmented Analytics API", version="0.1.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics/minute")
def minute_metrics(
    minutes: int = 60,
    action: Optional[str] = None,
    db: Session = Depends(get_db),
):
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    q = db.query(MinuteAgg).filter(MinuteAgg.minute_start >= cutoff)
    if action:
        q = q.filter(MinuteAgg.action == action)
    rows = q.order_by(MinuteAgg.minute_start.desc()).limit(500).all()
    return [
        {
            "minute_start": r.minute_start.isoformat(),
            "action": r.action,
            "count": r.count,
            "total_amount": r.total_amount,
        }
        for r in rows
    ]

@app.get("/insights")
def insights(minutes: int = 60, db: Session = Depends(get_db)):
    return generate_insight(db, minutes=minutes)
