from fastapi import APIRouter, Request, FastAPI, WebSocket, WebSocketDisconnect
from app.core import store
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.deps import get_db
from app.questions.schema import QuestionCreate
from app.user.model import User


class SurveyDoesntExist(Exception):
    pass


async def create_question(obj: QuestionCreate, current_user: User, db: AsyncSession = Depends(get_db)):
    survey = await store.survey.get(id=obj.article_id, db=db)
    if survey:
        question = await store.question.create_question(db=db, obj_in=obj, user_id=current_user.user_id)
    else:
        raise SurveyDoesntExist
    return question


async def get_question(db: AsyncSession = Depends(get_db)):
    question = await store.question.get_question_with_options(db=db, skip=0, limit=100)
    return question


class QuestionDoenstExist(Exception):
    pass


async def get_answers_from_question(question_id, db: AsyncSession = Depends(get_db)):
    question = await store.question.get(id=question_id, db=db)
    if question:
        answers = await store.question.get_by_question(question_id, db)
    else:
        raise QuestionDoenstExist
    return answers
