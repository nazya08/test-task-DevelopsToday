from datetime import datetime

from pydantic import BaseModel
from typing import Optional

from src.adapters.schemas.mission import MissionSpyCatShortResponse
from src.adapters.schemas.pagination import PaginationResponse


class SpyCatBase(BaseModel):
    name: str
    years_of_experience: Optional[int] = None
    breed: Optional[str] = None
    salary: Optional[float] = None


class SpyCatCreate(SpyCatBase):
    pass


class SpyCatUpdate(BaseModel):
    salary: Optional[float] = None


class SpyCatResponse(SpyCatBase):
    id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SpyCatShortResponse:
    id: int
    name: str
    breed: str


class SpyCatListResponse(BaseModel):
    pagination_detail: PaginationResponse
    spy_cats_list: list[SpyCatResponse]


class SpyCatExternalResponse(BaseModel):
    spy_cat_detail: SpyCatResponse
    missions: list[MissionSpyCatShortResponse]
    missions_count: int
