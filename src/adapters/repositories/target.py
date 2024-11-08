from typing import Optional

from sqlalchemy.exc import NoResultFound

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.sqlalchemy.models import Target
from src.adapters.repositories.common.target import TargetReader, TargetSaver


class TargetRepository(SQLAlchemyRepo, TargetSaver, TargetReader):
    def save_target(self, target: Target) -> None:
        self._session.add(target)
        self._session.commit()
        self._session.refresh(target)

    def update_target(self, target_id: int, target_data: dict) -> Optional[Target]:
        try:
            target = self.get_target_by_id(target_id)
            for key, value in target_data.items():
                setattr(target, key, value)
            self._session.commit()
            self._session.refresh(target)
            return target
        except NoResultFound:
            return None

    def delete_target(self, target_id: int) -> None:
        target = self.get_target_by_id(target_id)
        if target:
            self._session.delete(target)
            self._session.commit()

    def mark_target_as_completed(self, target_id: int) -> None:
        target = self.get_target_by_id(target_id)
        target.complete = True
        self._session.commit()

    def get_target_by_id(self, mission_id: int, target_id: int) -> Optional[Target]:
        return (
            self._session.query(Target)
            .filter(Target.mission_id == mission_id, Target.id == target_id)
            .first()
        )

    def get_all_targets_for_mission(self, mission_id: int) -> list[Target]:
        return self._session.query(Target).filter(Target.mission_id == mission_id).all()
