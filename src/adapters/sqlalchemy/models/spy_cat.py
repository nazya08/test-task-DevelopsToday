from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimeStampedModel


class SpyCat(Base, TimeStampedModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String, nullable=False, index=True)
    salary = Column(Float)

    missions = relationship("Mission", back_populates="spy_cat")
