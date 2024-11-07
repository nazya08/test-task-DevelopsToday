from fastapi import HTTPException

from src.adapters.repositories.mission import MissionRepository
from src.adapters.repositories.target import TargetRepository
from src.adapters.schemas.target import TargetUpdate
from src.adapters.sqlalchemy.models import Target


class TargetService:
    def __init__(self, target_repo: TargetRepository, mission_repo: MissionRepository):
        self.target_repo = target_repo
        self.mission_repo = mission_repo

    def update_target(self, target_id: int, obj_in: TargetUpdate) -> Target:
        target = self.target_repo.get_target_by_id(target_id)
        if not target:
            raise HTTPException(status_code=404, detail="Target not found.")

        if target.complete and (obj_in.notes or obj_in.dict(exclude_unset=True)):
            raise HTTPException(status_code=400, detail="Cannot update completed target.")

        mission = self.mission_repo.get_mission_by_id(target.mission_id)
        if mission and mission.complete and obj_in.notes:
            raise HTTPException(status_code=400, detail="Cannot update notes for a target in a completed mission.")

        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(target, key, value)

        self.target_repo.save_target(target)
        return target

    def mark_target_completed(self, target_id: int) -> None:
        target = self.target_repo.get_target_by_id(target_id)
        target.complete = True

        self.target_repo.save_target(target)
