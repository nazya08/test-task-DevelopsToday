from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK

from src.adapters.schemas.target import TargetResponse, TargetUpdate
from src.adapters.sqlalchemy.models import Target, Mission
from src.presentation.dependencies.mission import get_mission
from src.presentation.dependencies.target import get_target_service, get_target
from src.services.target import TargetService

router = APIRouter()


@router.put("/{mission_id}/targets/{target_id}", response_model=TargetResponse)
def update_target(
    target_in: TargetUpdate,
    mission: Mission = Depends(get_mission),
    target: Target = Depends(get_target),
    target_service: TargetService = Depends(get_target_service),
) -> TargetResponse:

    updated_target = target_service.update_target(target_id=target.id, obj_in=target_in)

    return TargetResponse(
        id=updated_target.id,
        mission_id=updated_target.mission_id,
        name=updated_target.name,
        country=updated_target.country,
        notes=updated_target.notes,
        complete=updated_target.complete,
        created_at=updated_target.created_at,
        updated_at=updated_target.updated_at
    )


@router.post("/{mission_id}/targets/{target_id}/complete", status_code=HTTP_200_OK)
def mark_target_completed(
    mission: Mission = Depends(get_mission),
    target: Target = Depends(get_target),
    target_service: TargetService = Depends(get_target_service),
) -> dict:

    target_service.mark_target_completed(target_id=target.id)

    return {"detail": "Target marked as completed."}
