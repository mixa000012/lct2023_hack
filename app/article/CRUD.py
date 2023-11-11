from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.CRUD import ModelAccessor, CreateSchemaType, ModelType
from app.article.model import Article
from app.questions.model import Question
from app.article.schema import ArticleBase, ArticleUpdate, ArticleCreate


class SurveyAccessor(ModelAccessor[Article, ArticleCreate, ArticleUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_questions(self, id, db: AsyncSession):
        survey = await db.execute(
            select(Article).options(selectinload(Article.questions).selectinload(Question.options)).where(Article.id == id)
        )
        survey = survey.scalar()
        return survey


survey = SurveyAccessor(Article)
