from abc import ABC, abstractmethod
from typing import Optional
from src.adapters.sqlalchemy.models import SpyCat


class SpyCatSaver(ABC):
    @abstractmethod
    def save_spy_cat(self, spy_cat: SpyCat) -> None:
        """Зберігає кота в базі даних."""
        raise NotImplementedError

    @abstractmethod
    def update_spy_cat(self, spy_cat_id: int, spy_cat_data: dict) -> Optional[SpyCat]:
        """Оновлює дані кота за його ID."""
        raise NotImplementedError

    @abstractmethod
    def delete_spy_cat(self, spy_cat_id: int) -> None:
        """Видаляє кота з бази даних за його ID."""
        raise NotImplementedError


class SpyCatReader(ABC):
    @abstractmethod
    def get_spy_cat_by_id(self, spy_cat_id: int) -> Optional[SpyCat]:
        """Отримує кота за його ID."""
        raise NotImplementedError

    @abstractmethod
    def get_all_spy_cats(self, skip: int = 0, limit: int = 10) -> list[SpyCat]:
        """Отримує список всіх котів."""
        raise NotImplementedError
