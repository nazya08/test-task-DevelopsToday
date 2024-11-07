from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.adapters.repositories.mission import MissionRepository
from src.adapters.repositories.target import TargetRepository
from src.adapters.sqlalchemy.models import Target
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.mission import get_mission_repo
from src.services.target import TargetService


def get_target_repo(db: Session = Depends(get_db)) -> TargetRepository:
    return TargetRepository(session=db)


def get_target_service(
        target_repo: TargetRepository = Depends(get_target_repo),
        mission_repo: MissionRepository = Depends(get_mission_repo)
) -> TargetService:
    return TargetService(target_repo=target_repo, mission_repo=mission_repo)


def get_target(target_id: int, target_repo: TargetRepository = Depends(get_target_repo)) -> Target:
    target = target_repo.get_target_by_id(target_id)
    if not target:
        raise HTTPException(
            status_code=404, detail="Target not found"
        )

    return target
