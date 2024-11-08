from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from src.adapters.schemas.mission import MissionCreate, MissionUpdate, MissionResponse, MissionListResponse, \
    MissionExternalResponse, MissionShortResponse, AssignMissionToSpyCat
from src.adapters.schemas.pagination import PaginationResponse
from src.adapters.schemas.target import TargetResponse
from src.presentation.dependencies.mission import get_mission_service
from src.presentation.dependencies.spy_cat import get_spy_cat_service
from src.services.mission import MissionService
from src.services.spy_cat import SpyCatService

router = APIRouter()


@router.post("/", response_model=MissionResponse)
def create_mission(
        mission_in: MissionCreate,
        mission_service: MissionService = Depends(get_mission_service),
) -> MissionResponse:
    mission = mission_service.create_mission(obj_in=mission_in)

    return MissionResponse(
        id=mission.id,
        spy_cat_id=mission.spy_cat_id,
        complete=mission.complete,
        created_at=mission.created_at,
        updated_at=mission.updated_at
    )


@router.patch("/{mission_id}/", response_model=MissionResponse)
def update_mission(
        mission_in: MissionUpdate,
        mission_id: int,
        spy_cat_id: int | None = None,
        mission_service: MissionService = Depends(get_mission_service),
) -> MissionResponse:
    mission = mission_service.update_mission(spy_cat_id=spy_cat_id, mission_id=mission_id, obj_in=mission_in)

    return MissionResponse(
        id=mission.id,
        spy_cat_id=mission.spy_cat_id,
        complete=mission.complete,
        created_at=mission.created_at,
        updated_at=mission.updated_at
    )


@router.delete("/{mission_id}/", status_code=HTTP_204_NO_CONTENT)
def delete_mission(
        mission_id: int,
        spy_cat_id: int | None = None,
        mission_service: MissionService = Depends(get_mission_service),
) -> None:
    return mission_service.delete_mission(spy_cat_id=spy_cat_id, mission_id=mission_id)


@router.get("/{mission_id}/", response_model=MissionExternalResponse)
def get_mission(
        mission_id: int,
        spy_cat_id: int | None = None,
        mission_service: MissionService = Depends(get_mission_service),
) -> MissionExternalResponse:

    if spy_cat_id:
        mission = mission_service.get_mission(spy_cat_id=spy_cat_id, mission_id=mission_id)
    else:
        mission = mission_service.get_mission(mission_id=mission_id)

    return MissionExternalResponse(
        mission_detail=MissionResponse(
            id=mission.id,
            spy_cat_id=mission.spy_cat_id,
            complete=mission.complete,
            created_at=mission.created_at,
            updated_at=mission.updated_at
        ),
        targets=[
            TargetResponse(
                id=target.id,
                mission_id=target.mission_id,
                name=target.name,
                country=target.country,
                notes=target.notes,
                complete=target.complete,
                created_at=target.created_at,
                updated_at=target.updated_at
            ) for target in mission.targets
        ],
        targets_count=len(mission.targets)
    )


@router.get("/", response_model=MissionListResponse)
def get_list_missions(
        spy_cat_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
        mission_service: MissionService = Depends(get_mission_service),
) -> MissionListResponse:

    if spy_cat_id:
        missions = mission_service.get_all_missions(spy_cat_id=spy_cat_id, skip=skip, limit=limit)
    else:
        missions = mission_service.get_all_missions(skip=skip, limit=limit)

    return MissionListResponse(
        pagination_detail=PaginationResponse(
            skip=skip,
            limit=limit,
            total=len(missions)
        ),
        missions_list=[
            MissionShortResponse(
                id=mission.id,
                spy_cat_id=mission.spy_cat_id,
                complete=mission.complete,
            ) for mission in missions
        ]
    )


@router.post("/{mission_id}/assign_cat/", status_code=HTTP_200_OK)
def assign_mission_to_cat(
        mission_id: int,
        mission_in: AssignMissionToSpyCat,
        mission_service: MissionService = Depends(get_mission_service),
        spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
) -> dict:

    spy_cat_id = mission_in.spy_cat_id

    mission = mission_service.get_mission(mission_id=mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    spy_cat = spy_cat_service.get_spy_cat(spy_cat_id=spy_cat_id)
    if not spy_cat:
        raise HTTPException(status_code=404, detail="SpyCat not found")

    mission_service.assign_cat_to_mission(spy_cat_id=spy_cat.id, mission_id=mission.id)

    return {"detail": f"Mission {mission.id} assigned to cat {spy_cat.id}"}
