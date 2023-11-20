from fastapi import APIRouter

from flatlandasp.features.environments import api as environments_api
from flatlandasp.features.solver import api as solver_api

router = APIRouter()

router.include_router(environments_api.router, prefix='/environments')
router.include_router(solver_api.router, prefix='/solver')
