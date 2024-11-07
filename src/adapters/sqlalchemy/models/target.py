from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimeStampedModel


class Target(Base, TimeStampedModel):
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("mission.id"))
    name = Column(String, nullable=False, index=True)
    country = Column(String)
    notes = Column(Text)
    complete = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")
