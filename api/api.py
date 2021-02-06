"""API module

"""
from fastapi import APIRouter

from api.routers.normapi import norm_api
from api.routers.yandex import ya
from api.routers.normalizer import normalizer

router = APIRouter()

router.include_router(norm_api)
router.include_router(ya)
router.include_router(normalizer)
