from typing import List
from uuid import UUID

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.user.auth.auth import get_current_user_from_token, get_device_id_from_token
from app.answers import service
from app.answers.service import QuestionDoenstExist
from app.answers.schema import AnswerCreate, AnswerBase, AnswerCreateWithId, AnswerShow
from app.user.model import User

router = APIRouter()


@router.post('/')
async def create_answer(option_ids: List[UUID], question_id: UUID, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    try:
        answer = await service.check_answers(db=db, current_user=current_user, option_ids=option_ids,
                                             question_id=question_id)
    except QuestionDoenstExist:
        raise HTTPException(status_code=422, detail="Question doesn't exists")
    return answer


@router.get('/')
async def get_by_question(question_id: UUID, db: AsyncSession = Depends(get_db)) -> List[AnswerShow]:
    try:
        answers = await service.get_answers_from_question(question_id, db)
    except QuestionDoenstExist:
        raise HTTPException(status_code=422, detail="Question doesn't exists")
    return answers
