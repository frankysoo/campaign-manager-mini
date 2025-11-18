from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    rules = Column(JSON, nullable=False)  # e.g., {"event_type": "purchase"}
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, unique=True, nullable=False)  # idempotency key
    payload = Column(JSON, nullable=False)
    campaign_triggers = Column(JSON, nullable=True)  # list of triggered campaign ids
    processed_at = Column(DateTime(timezone=True), nullable=True)
