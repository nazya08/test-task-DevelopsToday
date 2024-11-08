from abc import ABC, abstractmethod
from typing import Optional
from src.adapters.sqlalchemy.models import Mission


class MissionSaver(ABC):
    @abstractmethod
    def save_mission(self, mission: Mission) -> None:
        """Зберігає місію в базі даних."""
        raise NotImplementedError

    @abstractmethod
    def update_mission(self, spy_cat_id: int, mission_id: int, mission_data: dict) -> Optional[Mission]:
        """Оновлює дані місії за її ID."""
        raise NotImplementedError

    @abstractmethod
    def delete_mission(self, spy_cat_id: int, mission_id: int) -> None:
        """Видаляє місію за її ID."""
        raise NotImplementedError


class MissionReader(ABC):
    @abstractmethod
    def get_mission_by_id(self, spy_cat_id: int, mission_id: int) -> Optional[Mission]:
        """Отримує місію за її ID."""
        raise NotImplementedError

    @abstractmethod
    def get_all_missions(self, spy_cat_id: int, skip: int = 0, limit: int = 10) -> list[Mission]:
        """Отримує список всіх місій."""
        raise NotImplementedError
