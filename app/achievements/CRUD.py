from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.CRUD import ModelAccessor
from app.user.model import Roles
from app.achievements.model import Achievements
from app.achievements.schema import AchievementCreate
from app.achievements.schema import AchievementsUpdate


class AchievementsAccessor(ModelAccessor[Achievements, AchievementCreate, AchievementsUpdate]):
    pass

    async def get_by_title(self, title, db: AsyncSession):
        achievement = await db.execute(select(Achievements).where(Achievements.title == title))
        achievement = achievement.scalar()
        return achievement
    #
    # async def get_role(self, db: AsyncSession, role):
    #     role = await db.execute(select(Roles).where(Roles.role == role))
    #     role = role.scalar()
    #     return role
    #
    # async def get(self, db: AsyncSession, user_id):
    #     stmt = (
    #         select(User)
    #         .options(selectinload(User.admin_role))
    #         .where(User.user_id == user_id)
    #     )
    #     user = await db.execute(stmt)
    #     user = user.scalar()
    #     return user


achievements = AchievementsAccessor(Achievements)
