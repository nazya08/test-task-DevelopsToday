from fastapi import APIRouter
from src.presentation.api.spy_cat import routers as spy_cat_routers
from src.presentation.api.mission import routers as mission_routers
from src.presentation.api.targets import routers as target_routers

api_router = APIRouter()

api_router.include_router(spy_cat_routers.router, prefix="/spy-cats", tags=["spy-cat"])
api_router.include_router(mission_routers.router, prefix="/missions", tags=["mission"])
api_router.include_router(target_routers.router, prefix="/missions", tags=["target"])


@api_router.get("/alive")
def alive():
    return {'status': 'ok'}
