from typing import Optional

from src.adapters.schemas.spy_cat import SpyCatCreate, SpyCatUpdate
from src.adapters.sqlalchemy.models import SpyCat
from src.adapters.repositories.spy_cat import SpyCatRepository


class SpyCatService:
    def __init__(self, spy_cat_repo: SpyCatRepository):
        self.spy_cat_repo = spy_cat_repo

    def create_spy_cat(self, obj_in: SpyCatCreate) -> SpyCat:
        """Створює нового кота."""

        # TODO: Add validation
        spy_cat_data = obj_in.dict()
        spy_cat = SpyCat(**spy_cat_data)
        self.spy_cat_repo.save_spy_cat(spy_cat)

        return spy_cat

    def update_spy_cat(self, spy_cat_id: int, obj_in: SpyCatUpdate) -> Optional[SpyCat]:
        """Оновлює дані кота за його ID."""
        return self.spy_cat_repo.update_spy_cat(spy_cat_id, obj_in.dict())

    def delete_spy_cat(self, spy_cat_id: int) -> None:
        """Видаляє кота за його ID."""

        self.spy_cat_repo.delete_spy_cat(spy_cat_id)

    def get_spy_cat(self, spy_cat_id: int) -> Optional[SpyCat]:
        """Отримує кота за його ID."""

        return self.spy_cat_repo.get_spy_cat_by_id(spy_cat_id)

    def list_spy_cats(self, skip: int = 0, limit: int = 10) -> list[SpyCat]:
        """Отримує список всіх котів."""

        return self.spy_cat_repo.get_all_spy_cats(skip, limit)
