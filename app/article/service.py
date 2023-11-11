from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.deps import get_db
from app.core import store
from app.article.schema import ArticleCreate, ArticleShow
from app.user.model import User


async def create_arcticle(obj_in: ArticleCreate, current_user: User, db: AsyncSession = Depends(get_db)) -> ArticleShow:
    obj_in_dict = obj_in.dict()
    obj_in_dict["created_by"] = current_user.user_id
    return await store.survey.create(db, obj_in=obj_in_dict)


async def get_questions(id, db: AsyncSession):
    questions = await store.survey.get_questions(id=id, db=db)
    return questions
