from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.CRUD import ModelAccessor
from app.statistics.schema import StatisticsCreate, StatisticsUpdate
from app.statistics.model import Statistics


class StatisticsAccessor(ModelAccessor[Statistics, StatisticsCreate, StatisticsUpdate]):
    async def get_statistic(self, user_id: UUID, db: AsyncSession):
        stmt = select(Statistics).where(Statistics.user_id == user_id)
        statistic = await db.execute(stmt)
        statistic = statistic.scalars().all()

        return statistic

    async def get_statistic_by_article(self, user_id: UUID, db: AsyncSession, article_id):
        stmt = select(Statistics).where(and_(Statistics.user_id == user_id, Statistics.article_id == article_id))
        statistic = await db.execute(stmt)
        statistic = statistic.scalars().all()

        return statistic


# async def create_question(self, db: AsyncSession, obj_in: QuestionCreate, user_id: UUID):
#     question_ = QuestionCreate(text=obj_in.text, options=[], article_id=obj_in.article_id)
#     for option_data in obj_in.options:
#         option = Option(text=option_data.text)
#         question_.options.append(option)
#     obj_in_data = question_.dict()
#     db_obj = self.model(**obj_in_data)  # type: ignore
#     db.add(db_obj)
#     await db.commit()
#     return db_obj
#

#
# async def get_option(self, db: AsyncSession, option_id):
#     option = await db.execute(select(Option).where(Option.id == option_id))
#     option = option.scalar()
#     return option
#


statistics = StatisticsAccessor(Statistics)
