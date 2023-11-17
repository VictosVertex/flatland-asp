from fastapi import APIRouter

from flatlandasp.features.environments import api as environments_api

router = APIRouter()

router.include_router(environments_api.router, prefix='/environments')
