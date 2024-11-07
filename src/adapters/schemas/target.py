from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class TargetBase(BaseModel):
    name: str
    country: Optional[str] = None
    notes: Optional[str] = None
    complete: Optional[bool] = False


class TargetCreate(TargetBase):
    mission_id: int


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    complete: Optional[bool] = False


class TargetResponse(TargetBase):
    id: int
    mission_id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
