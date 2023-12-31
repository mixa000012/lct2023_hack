import uuid
from datetime import datetime

from pydantic.main import BaseModel


class AchievementBase(BaseModel):
    description: str
    title: str

    class Config:
        orm_mode = True


class AchievementFile(AchievementBase):
    pass


class AchievementCreate(AchievementBase):
    image: str


class AchievementsUpdate(AchievementBase):
    pass


class AchievementShow(AchievementBase):
    created_at: datetime
    id: uuid.UUID
