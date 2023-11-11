from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.answers.model import Answer
from app.answers.schema import AnswerCreate, AnswerUpdate
from app.core.db.CRUD import ModelAccessor
from app.questions.model import Option


class AnswerAccessor(ModelAccessor[Answer, AnswerCreate, AnswerUpdate]):
    async def create(self, db: AsyncSession, *, db_obj):
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_question_with_text(self, question_id, db):
        stmt = select(Answer).where(and_(Answer.text != 'null', Answer.question_id == question_id))
        answers = await db.execute(stmt)
        answers = answers.scalars().all()

        return answers

    async def is_exist(self, user_id, db, option_id):
        stmt = select(Answer).where(and_(Answer.user_id == user_id, Answer.option_id == option_id))
        answers = await db.execute(stmt)
        answers = answers.scalars().all()
        if answers:
            return True
        else:
            return False

    async def get_by_question(self, question_id, db):
        stmt = select(Answer).where(Answer.question_id == question_id)
        answers = await db.execute(stmt)
        answers = answers.scalars().all()

        return answers

    async def get_count_answers(self, user_id, db, question_id):
        stmt = select(Answer).join(Option).where(
            and_(Answer.user_id == user_id, Option.is_correct == True, Option.question_id == question_id))
        answers = await db.execute(stmt)
        answers = answers.scalars().all()
        print(answers)
        return answers


answer = AnswerAccessor(Answer)
