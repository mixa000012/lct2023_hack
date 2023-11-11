from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import store
from app.core.deps import get_db
from app.statistics.schema import StatisticsCreate, StatisticsUpdate
from app.user.model import User


class SurveyDoesntExist(Exception):
    pass


async def create_statistics(obj: StatisticsCreate, current_user: User, db: AsyncSession = Depends(get_db)):
    obj_in_dict = obj.dict()
    obj_in_dict["user_id"] = current_user.user_id
    obj_ = StatisticsCreate(**obj_in_dict)
    question = await store.statistics.create(db=db, obj_in=obj_)
    return question


async def get_statistic(current_user: User, db: AsyncSession):
    statistic = await store.statistics.get_statistic(db=db, user_id=current_user.user_id)
    return statistic


async def get_statistic_by_article(article_id: UUID, current_user: User, db: AsyncSession):
    statistic = await store.statistics.get_statistic_by_article(db=db, user_id=current_user.user_id,
                                                                article_id=article_id)
    return statistic


class QuestionDoenstExist(Exception):
    pass
