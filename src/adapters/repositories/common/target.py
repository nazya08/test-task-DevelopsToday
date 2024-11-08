from abc import ABC, abstractmethod
from typing import Optional
from src.adapters.sqlalchemy.models import Target


class TargetSaver(ABC):
    @abstractmethod
    def save_target(self, target: Target) -> None:
        """Зберігає ціль в базі даних."""
        raise NotImplementedError

    @abstractmethod
    def update_target(self, target_id: int, target_data: dict) -> Optional[Target]:
        """Оновлює дані цілі за її ID."""
        raise NotImplementedError

    @abstractmethod
    def delete_target(self, target_id: int) -> None:
        """Видаляє ціль за її ID."""
        raise NotImplementedError

    @abstractmethod
    def mark_target_as_completed(self, target_id: int) -> None:
        """Позначає ціль як завершену."""
        raise NotImplementedError


class TargetReader(ABC):
    @abstractmethod
    def get_target_by_id(self, mission_id: int, target_id: int) -> Optional[Target]:
        """Отримує ціль за її ID."""
        raise NotImplementedError

    @abstractmethod
    def get_all_targets_for_mission(self, mission_id: int) -> list[Target]:
        """Отримує всі цілі для конкретної місії."""
        raise NotImplementedError
