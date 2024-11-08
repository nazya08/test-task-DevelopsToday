from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimeStampedModel:
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
