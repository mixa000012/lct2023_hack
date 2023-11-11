from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.answers.model import Answer
from app.core.db.CRUD import ModelAccessor
from app.answers.schema import AnswerCreate, AnswerUpdate


class AnswerAccessor(ModelAccessor[Answer, AnswerCreate, AnswerUpdate]):
    async def create(self, db: AsyncSession, *, obj_in):
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_question_with_text(self, question_id, db):
        stmt = select(Answer).where(and_(Answer.text != 'null', Answer.question_id == question_id))
        answers = await db.execute(stmt)
        answers = answers.scalars().all()

        return answers

    async def get_by_question(self, question_id, db):
        stmt = select(Answer).where(Answer.question_id == question_id)
        answers = await db.execute(stmt)
        answers = answers.scalars().all()

        return answers


answer = AnswerAccessor(Answer)
