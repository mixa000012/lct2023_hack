import json
from openai import OpenAI

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.questions import service
from app.questions.schema import QuestionCreate, QuestionBase, QuestionShow, GenerateQuiz
from app.questions.service import SurveyDoesntExist
from app.user.auth.auth import get_current_user_from_token
from app.user.model import User
from app.core.config import settings

router = APIRouter()


@router.post('/')
async def create_question(obj: QuestionCreate, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user_from_token)) -> QuestionShow:
    try:
        question = await service.create_question(obj=obj, db=db, current_user=current_user)
    except SurveyDoesntExist:
        raise HTTPException(status_code=422, detail="Survey doesn't exists")
    return question


@router.post('/create_quiz')
def create_json_quiz(obj: GenerateQuiz):
    return service.generate_quiz(obj)
