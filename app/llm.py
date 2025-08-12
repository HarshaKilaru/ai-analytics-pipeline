from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import MinuteAgg

# For v0 we build a simple heuristic "insight".
# Later you can swap this for a real LLM call.

def generate_insight(db: Session, minutes: int = 60) -> dict:
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    # Top action by count
    top = (
        db.query(MinuteAgg.action, func.sum(MinuteAgg.count).label("c"))
        .filter(MinuteAgg.minute_start >= cutoff)
        .group_by(MinuteAgg.action)
        .order_by(func.sum(MinuteAgg.count).desc())
        .first()
    )

    # Total purchase amount
    total_sales = (
        db.query(func.sum(MinuteAgg.total_amount))
        .filter(MinuteAgg.minute_start >= cutoff, MinuteAgg.action == "purchase")
        .scalar()
        or 0.0
    )

    if top:
        summary = (
            f"In the last {minutes} minutes, '{top.action}' leads with ~{int(top.c)} events. "
            f"Estimated revenue from purchases is ${total_sales:,.2f}."
        )
    else:
        summary = f"No data yet for the last {minutes} minutes."

    return {
        "window_minutes": minutes,
        "top_action": top.action if top else None,
        "total_sales": round(float(total_sales), 2),
        "summary": summary,
    }
