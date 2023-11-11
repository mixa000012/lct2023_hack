from uuid import UUID

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.questions import service
from app.questions.service import SurveyDoesntExist

from app.core import store

from app.questions.schema import QuestionCreate, QuestionBase
from app.user.auth.auth import get_current_user_from_token
from app.user.model import User

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.post('/')
async def create_question(obj: QuestionCreate, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user_from_token)) -> QuestionBase:
    try:
        question = await service.create_question(obj=obj, db=db, current_user=current_user)
    except SurveyDoesntExist:
        raise HTTPException(status_code=422, detail="Survey doesn't exists")
    return question
