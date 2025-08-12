from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from .db import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    action = Column(String, index=True)           # "click", "view", "purchase"
    product = Column(String, index=True)
    amount = Column(Float)                         # only used for purchase
    ts = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class MinuteAgg(Base):
    __tablename__ = "minute_agg"
    id = Column(Integer, primary_key=True, index=True)
    minute_start = Column(DateTime(timezone=True), index=True)
    action = Column(String, index=True)
    count = Column(Integer)
    total_amount = Column(Float)   # sum of purchase amounts in that minute (0 for others)
