from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.CRUD import ModelAccessor, CreateSchemaType, ModelType
from app.article.model import Article, Deadlines
from app.questions.model import Question
from app.article.schema import ArticleBase, ArticleUpdate, ArticleCreate
from app.user.model import User


class SurveyAccessor(ModelAccessor[Article, ArticleCreate, ArticleUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_questions(self, id, db: AsyncSession):
        survey = await db.execute(
            select(Article).options(selectinload(Article.questions).selectinload(Question.options)).where(
                Article.id == id)
        )
        survey = survey.scalar()
        return survey

    async def get_deadlines_from_user(self, db: AsyncSession, current_user: User):
        articles = await db.execute(
            select(Deadlines).options(selectinload(Deadlines.articles)).where(
                Article.created_by == current_user.user_id)
        )
        articles = articles.scalars().all()
        return articles

    async def get_deadline(self, db: AsyncSession, current_user: User, survey_id):
        articles = await db.execute(
            select(Deadlines).options(selectinload(Deadlines.articles)).where(and_(
                Article.created_by == current_user.user_id), Article.id == survey_id)
        )
        articles = articles.scalars().all()
        return articles


survey = SurveyAccessor(Article)
