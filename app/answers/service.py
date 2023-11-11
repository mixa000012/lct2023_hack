from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.answers.model import Answer
from app.answers.schema import AnswerCreate, AnswerShow
from app.core import store
from app.core.deps import get_db
from app.user.model import User


class QuestionDoenstExist(Exception):
    pass


async def get_answers_from_question(question_id, db: AsyncSession = Depends(get_db)):
    question = await store.question.get(id=question_id, db=db)
    if question:
        answers = await store.question.get_by_question(question_id, db)
    else:
        raise QuestionDoenstExist
    return answers


async def check_answers(option_ids: List[UUID], current_user: User, question_id: UUID,
                        db: AsyncSession = Depends(get_db)):
    for option_id in option_ids:
        answer = Answer(option_id=option_id, user_id=current_user.user_id, is_answered=True)
        if not await store.answer.is_exist(db=db, user_id=current_user.user_id, option_id=option_id):
            await store.answer.create(db=db, db_obj=answer)
    correct_answers = await store.answer.get_count_answers(user_id=current_user.user_id, db=db, question_id=question_id)
    current_user.exp += len(correct_answers) * 5
    await db.commit()
    return len(correct_answers)


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
