from fastapi import APIRouter

from app.api.v1.endpoints import user, achievements

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
