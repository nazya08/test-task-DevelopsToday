from fastapi import HTTPException

from src.adapters.repositories.mission import MissionRepository
from src.adapters.repositories.spy_cat import SpyCatRepository
from src.adapters.schemas.mission import MissionUpdate, MissionCreate
from src.adapters.sqlalchemy.models import Mission


class MissionService:
    def __init__(self, spy_cat_repo: SpyCatRepository, mission_repo: MissionRepository):
        self.spy_cat_repo = spy_cat_repo
        self.mission_repo = mission_repo

    def get_all_missions(self, spy_cat_id: int | None = None, skip: int = 0, limit: int = 10) -> list[Mission]:
        if spy_cat_id:
            spy_cat = self.spy_cat_repo.get_spy_cat_by_id(spy_cat_id)
            if not spy_cat:
                raise HTTPException(
                    status_code=404,
                    detail="SpyCat not found"
                )
        return self.mission_repo.get_all_missions(spy_cat_id=spy_cat_id, skip=skip, limit=limit)

    def get_mission(self, mission_id: int, spy_cat_id: int | None = None) -> Mission:
        if spy_cat_id:
            spy_cat = self.spy_cat_repo.get_spy_cat_by_id(spy_cat_id)
            if not spy_cat:
                raise HTTPException(
                    status_code=404,
                    detail="SpyCat not found"
                )

        mission = self.mission_repo.get_mission_by_id(spy_cat_id=spy_cat_id, mission_id=mission_id)
        if not mission:
            raise HTTPException(
                status_code=404,
                detail="Mission not found"
            )

        return mission

    def create_mission(self, obj_in: MissionCreate) -> Mission:
        mission_data = obj_in.dict(exclude_unset=True)

        if obj_in.spy_cat_id:
            mission_data['spy_cat_id'] = obj_in.spy_cat_id
        else:
            mission_data['spy_cat_id'] = None

        mission_obj = Mission(**mission_data)
        self.mission_repo.save_mission(mission_obj)

        return mission_obj

    def update_mission(self, mission_id: int, obj_in: MissionUpdate, spy_cat_id: int | None = None) -> Mission:
        mission = self.get_mission(spy_cat_id=spy_cat_id, mission_id=mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="Mission not found")

        if spy_cat_id:
            spy_cat = self.spy_cat_repo.get_spy_cat_by_id(spy_cat_id)
            if not spy_cat:
                raise HTTPException(status_code=404, detail="SpyCat not found")

        return self.mission_repo.update_mission(
            spy_cat_id=spy_cat_id,
            mission_id=mission_id,
            mission_data=obj_in.dict()
        )

    def assign_cat_to_mission(self, spy_cat_id: int, mission_id: int) -> None:
        mission = self.mission_repo.get_mission_by_id(mission_id=mission_id)
        if not mission:
            raise HTTPException(
                status_code=404,
                detail=f"Mission with ID {mission_id} not found."
            )

        if mission.spy_cat_id is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Mission {mission.id} is already assigned to a cat with ID {mission.spy_cat_id}."
            )

        mission.spy_cat_id = spy_cat_id
        self.mission_repo.save_mission(mission)

    def delete_mission(self, mission_id: int, spy_cat_id: int | None = None) -> None:
        mission = self.get_mission(spy_cat_id=spy_cat_id, mission_id=mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="Mission not found")

        if spy_cat_id:
            spy_cat = self.spy_cat_repo.get_spy_cat_by_id(spy_cat_id)
            if not spy_cat:
                raise HTTPException(status_code=404, detail="SpyCat not found")

        if mission.spy_cat_id is not None:
            raise HTTPException(status_code=400, detail="Mission cannot be deleted as it is assigned to a spy cat.")

        self.mission_repo.delete_mission(spy_cat_id=spy_cat_id, mission_id=mission_id)

