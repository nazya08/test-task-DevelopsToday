from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.adapters.repositories.mission import MissionRepository
from src.adapters.repositories.spy_cat import SpyCatRepository
from src.adapters.sqlalchemy.models import Mission
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.spy_cat import get_spy_cat_repo
from src.services.mission import MissionService


def get_mission_repo(db: Session = Depends(get_db)) -> MissionRepository:
    return MissionRepository(session=db)


def get_mission_service(
        spy_cat_repo: SpyCatRepository = Depends(get_spy_cat_repo),
        mission_repo: MissionRepository = Depends(get_mission_repo)
) -> MissionService:
    return MissionService(spy_cat_repo=spy_cat_repo, mission_repo=mission_repo)


def get_mission(mission_id: int, spy_cat_id: int | None = None, mission_repo: MissionRepository = Depends(get_mission_repo)) -> Mission:
    mission = mission_repo.get_mission_by_id(spy_cat_id=spy_cat_id, mission_id=mission_id)
    if not mission:
        raise HTTPException(
            status_code=404, detail="Mission not found"
        )

    return mission
