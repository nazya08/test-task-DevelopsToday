from typing import Optional

from sqlalchemy.exc import NoResultFound

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.repositories.common.spy_cat import SpyCatSaver, SpyCatReader
from src.adapters.sqlalchemy.models import SpyCat


class SpyCatRepository(SQLAlchemyRepo, SpyCatSaver, SpyCatReader):
    def save_spy_cat(self, spy_cat: SpyCat) -> None:
        self._session.add(spy_cat)
        self._session.commit()
        self._session.refresh(spy_cat)

    def update_spy_cat(self, spy_cat_id: int, spy_cat_data: dict) -> Optional[SpyCat]:
        try:
            spy_cat = self.get_spy_cat_by_id(spy_cat_id)
            for key, value in spy_cat_data.items():
                setattr(spy_cat, key, value)
            self._session.commit()
            self._session.refresh(spy_cat)
            return spy_cat
        except NoResultFound:
            return None

    def delete_spy_cat(self, spy_cat_id: int) -> None:
        spy_cat = self.get_spy_cat_by_id(spy_cat_id)
        if spy_cat:
            self._session.delete(spy_cat)
            self._session.commit()

    def get_spy_cat_by_id(self, spy_cat_id: int) -> Optional[SpyCat]:
        return self._session.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()

    def get_all_spy_cats(self, skip: int = 0, limit: int = 10) -> list[SpyCat]:
        return self._session.query(SpyCat).offset(skip).limit(limit).all()
