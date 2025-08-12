import time, random
from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session
from .db import engine, Base, SessionLocal
from .models import Event
from .config import EVENTS_PER_SEC

fake = Faker()
ACTIONS = ["view", "click", "purchase"]

def ensure_tables():
    Base.metadata.create_all(bind=engine)

def generate_event():
    action = random.choices(ACTIONS, weights=[0.6, 0.3, 0.1])[0]
    return Event(
        user_id=fake.uuid4(),
        action=action,
        product=fake.word(),
        amount=round(random.uniform(5, 200), 2) if action == "purchase" else 0.0,
        ts=datetime.utcnow(),
    )

def run_ingest():
    ensure_tables()
    print("[ingest] starting event generator…")
    per_event_sleep = 1.0 / max(EVENTS_PER_SEC, 1)
    with SessionLocal() as db:
        while True:
            ev = generate_event()
            db.add(ev)
            db.commit()
            time.sleep(per_event_sleep)

if __name__ == "__main__":
    run_ingest()
