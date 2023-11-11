from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.article.model import Article
from app.core.db.CRUD import ModelAccessor
from app.questions.model import Question, Option
from app.questions.schema import QuestionCreate, QuestionUpdate


class QuestionAccessor(ModelAccessor[Question, QuestionCreate, QuestionUpdate]):
    async def create_question(self, db: AsyncSession, obj_in: QuestionCreate, user_id: UUID):
        question_ = QuestionCreate(text=obj_in.text, options=[], article_id=obj_in.article_id)
        for option_data in obj_in.options:
            option = Option(text=option_data.text, is_correct=option_data.is_correct)
            question_.options.append(option)
        obj_in_data = question_.dict()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_question_with_options(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100, article_id: UUID
    ):
        stmt = select(Question).options(selectinload(Question.options)).where(Article.id == article_id).offset(
            skip).limit(limit)

        question = await db.execute(stmt)
        questions = question.scalars().all()

        return questions

    async def get_option(self, db: AsyncSession, option_id):
        option = await db.execute(select(Option).where(Option.id == option_id))
        option = option.scalar()
        return option

    async def get_by_question(self, question_id, db):
        stmt = select(Option).where(Option.question_id == question_id)
        answers = await db.execute(stmt)
        answers = answers.scalars().all()

        return answers


question = QuestionAccessor(Question)
