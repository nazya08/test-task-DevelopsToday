from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimeStampedModel


class Mission(Base, TimeStampedModel):
    id = Column(Integer, primary_key=True, index=True)
    spy_cat_id = Column(Integer, ForeignKey("spycat.id"))
    complete = Column(Boolean, default=False)

    spy_cat = relationship("SpyCat", back_populates="missions")
    targets = relationship("Target", back_populates="mission")

