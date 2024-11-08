from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from src.adapters.schemas.pagination import PaginationResponse
from src.adapters.schemas.target import TargetResponse


class MissionBase(BaseModel):
    spy_cat_id: Optional[int] = None
    complete: Optional[bool] = False


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    complete: Optional[bool] = None


class MissionResponse(MissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MissionShortResponse(BaseModel):
    id: int
    spy_cat_id: int | None
    complete: bool


class MissionSpyCatShortResponse(BaseModel):
    id: int
    complete: bool


class MissionExternalResponse(BaseModel):
    mission_detail: MissionResponse
    targets: list[TargetResponse]
    targets_count: int


class MissionListResponse(BaseModel):
    pagination_detail: PaginationResponse
    missions_list: list[MissionShortResponse]


class AssignMissionToSpyCat(BaseModel):
    spy_cat_id: int
