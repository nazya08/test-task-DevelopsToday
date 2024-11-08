from typing import Optional

from sqlalchemy.exc import NoResultFound

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.repositories.common.mission import MissionSaver, MissionReader
from src.adapters.sqlalchemy.models import Mission


class MissionRepository(SQLAlchemyRepo, MissionSaver, MissionReader):
    def save_mission(self, mission: Mission) -> None:
        self._session.add(mission)
        self._session.commit()
        self._session.refresh(mission)

    def update_mission(self, spy_cat_id: int | None, mission_id: int, mission_data: dict) -> Optional[Mission]:
        try:
            mission = self.get_mission_by_id(spy_cat_id=spy_cat_id, mission_id=mission_id)
            for key, value in mission_data.items():
                setattr(mission, key, value)
            self._session.commit()
            self._session.refresh(mission)
            return mission
        except NoResultFound:
            return None

    def delete_mission(self, spy_cat_id: int | None, mission_id: int) -> None:
        mission = self.get_mission_by_id(spy_cat_id=spy_cat_id, mission_id=mission_id)
        if mission:
            self._session.delete(mission)
            self._session.commit()

    def get_mission_by_id(self, mission_id: int, spy_cat_id: int | None = None) -> Optional[Mission]:
        query = self._session.query(Mission).filter(Mission.id == mission_id)

        if spy_cat_id is not None:
            query = query.filter(Mission.spy_cat_id == spy_cat_id, Mission.id == mission_id)

        return query.first()

    def get_all_missions(self, spy_cat_id: int | None = None, skip: int = 0, limit: int = 10) -> list[Mission]:
        query = self._session.query(Mission)

        if spy_cat_id is not None:
            query = query.filter(Mission.spy_cat_id == spy_cat_id)

        return query.offset(skip).limit(limit).all()
