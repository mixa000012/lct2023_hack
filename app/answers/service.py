from fastapi import APIRouter, Request, FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.deps import get_db
from app.core import store
from app.answers.schema import AnswerCreate, AnswerShow, AnswerCreateWithId
from app.user.auth.auth import get_current_user_from_token, get_device_id_from_token
from app.user.model import User


class QuestionDoenstExist(Exception):
    pass


async def create_answer(obj: AnswerCreate, current_user: User, db: AsyncSession = Depends(get_db)) -> AnswerShow:
    question = await store.question.get(id=obj.question_id, db=db)
    option = await store.question.get_option(db=db, option_id=obj.option_id)
    if question and option:
        obj_in_dict = obj.dict()
        obj_in_dict["user_id"] = current_user.user_id
    else:
        raise QuestionDoenstExist
    return await store.answer.create(db, obj_in=obj_in_dict)


async def get_answers_from_question_with_text(question_id, db: AsyncSession = Depends(get_db)):
    question = await store.question.get(id=question_id, db=db)
    if question:
        answers = await store.question.get_by_question_with_text(question_id, db)
    else:
        raise QuestionDoenstExist
    return answers


