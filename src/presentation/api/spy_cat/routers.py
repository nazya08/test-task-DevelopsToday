from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from src.adapters.schemas.mission import MissionSpyCatShortResponse
from src.adapters.schemas.pagination import PaginationResponse
from src.adapters.sqlalchemy.models import SpyCat
from src.adapters.schemas.spy_cat import SpyCatCreate, SpyCatUpdate, SpyCatResponse, SpyCatExternalResponse, \
    SpyCatListResponse
from src.presentation.dependencies.spy_cat import get_spy_cat_service, get_spy_cat
from src.services.cat_breed_validator import cat_breed_validator
from src.services.spy_cat import SpyCatService


router = APIRouter()


@router.post(
    "/",
    response_model=SpyCatResponse,
    description="When creating a spy cat, you need to provide the valid breed_id, not the breed name."
)
def create_spy_cat(
        *,
        spy_cat_service: SpyCatService = Depends(get_spy_cat_service),
        spy_cat_in: SpyCatCreate,
) -> SpyCatResponse:

    cat_breed_validator.validate_breed(breed_id=spy_cat_in.breed)
    spy_cat = spy_cat_service.create_spy_cat(obj_in=spy_cat_in)

    return SpyCatResponse(
        id=spy_cat.id,
        name=spy_cat.name,
        years_of_experience=spy_cat.years_of_experience,
        breed=spy_cat.breed,
        salary=spy_cat.salary,
        created_at=spy_cat.created_at,
        updated_at=spy_cat.updated_at
    )


@router.put("/{spy_cat_id}/", response_model=SpyCatResponse)
def update_spy_cat(
        spy_cat_in: SpyCatUpdate,
        spy_cat: SpyCat = Depends(get_spy_cat),
        spy_cat_service: SpyCatService = Depends(get_spy_cat_service),
) -> SpyCatResponse:

    updated_spy_cat = spy_cat_service.update_spy_cat(spy_cat_id=spy_cat.id, obj_in=spy_cat_in)

    return SpyCatResponse(
        id=updated_spy_cat.id,
        name=updated_spy_cat.name,
        years_of_experience=updated_spy_cat.years_of_experience,
        breed=updated_spy_cat.breed,
        salary=updated_spy_cat.salary,
        created_at=updated_spy_cat.created_at,
        updated_at=updated_spy_cat.updated_at
    )


@router.delete("/{spy_cat_id}/", status_code=HTTP_204_NO_CONTENT)
def delete_spy_cat(
        spy_cat: SpyCat = Depends(get_spy_cat),
        spy_cat_service: SpyCatService = Depends(get_spy_cat_service),
) -> None:

    return spy_cat_service.delete_spy_cat(spy_cat_id=spy_cat.id)


@router.get("/{spy_cat_id}/", response_model=SpyCatExternalResponse)
def get_spy_cat(
        spy_cat: SpyCat = Depends(get_spy_cat),
        spy_cat_service: SpyCatService = Depends(get_spy_cat_service),
) -> SpyCatExternalResponse:

    spy_cat = spy_cat_service.get_spy_cat(spy_cat_id=spy_cat.id)

    return SpyCatExternalResponse(
        spy_cat_detail=SpyCatResponse(
            id=spy_cat.id,
            name=spy_cat.name,
            years_of_experience=spy_cat.years_of_experience,
            breed=spy_cat.breed,
            salary=spy_cat.salary,
            created_at=spy_cat.created_at,
            updated_at=spy_cat.updated_at
        ),
        missions=[
            MissionSpyCatShortResponse(
                id=mission.id,
                complete=mission.complete
            ) for mission in spy_cat.missions
        ],
        missions_count=len(spy_cat.missions)
    )


@router.get("/", response_model=SpyCatListResponse)
def get_list_spy_cats(
        skip: int = 0,
        limit: int = 10,
        spy_cat_service: SpyCatService = Depends(get_spy_cat_service),
) -> SpyCatListResponse:

    spy_cats = spy_cat_service.list_spy_cats(skip, limit)

    return SpyCatListResponse(
        pagination_detail=PaginationResponse(
            skip=skip,
            limit=limit,
            total=len(spy_cats)
        ),
        spy_cats_list=[
            SpyCatResponse(
                id=spy_cat.id,
                name=spy_cat.name,
                years_of_experience=spy_cat.years_of_experience,
                breed=spy_cat.breed,
                salary=spy_cat.salary,
                created_at=spy_cat.created_at,
                updated_at=spy_cat.updated_at
            ) for spy_cat in spy_cats
        ]
    )
