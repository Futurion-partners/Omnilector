from fastapi import APIRouter

from .image import router as image_router
from .realtime import router as realtime_router

v1_router = APIRouter(
    prefix='/v1',
)

v1_router.include_router(
    image_router
)

v1_router.include_router(
    realtime_router
)

@v1_router.get("/version")
async def get_version():
    """Return the current version of the API."""
    return {"version": "1.0.0", "name": "omnilector"}

__all__ = ['v1_router']
