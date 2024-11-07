from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.adapters.repositories.spy_cat import SpyCatRepository
from src.adapters.sqlalchemy.models import SpyCat
from src.services.spy_cat import SpyCatService
from src.presentation.dependencies.base import get_db


def get_spy_cat_repo(db: Session = Depends(get_db)) -> SpyCatRepository:
    return SpyCatRepository(session=db)


def get_spy_cat_service(
        spy_cat_repo: SpyCatRepository = Depends(get_spy_cat_repo),
) -> SpyCatService:
    return SpyCatService(spy_cat_repo=spy_cat_repo)


def get_spy_cat(spy_cat_id: int, spy_cat_repo: SpyCatRepository = Depends(get_spy_cat_repo)) -> SpyCat:
    spy_cat = spy_cat_repo.get_spy_cat_by_id(spy_cat_id)
    if not spy_cat:
        raise HTTPException(
            status_code=404, detail="SpyCat not found"
        )

    return spy_cat
