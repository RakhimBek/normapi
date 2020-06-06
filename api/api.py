"""API module

"""
from fastapi import APIRouter

from api.routers.normapi import norm_api

router = APIRouter()

router.include_router(norm_api)
