from fastapi import APIRouter

from app.api.v1.endpoints import user, questions, answer, survey, achievements

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
api_router.include_router(answer.router, prefix="/answer", tags=["answer"])
api_router.include_router(survey.router, prefix="/survey", tags=["survey"])
