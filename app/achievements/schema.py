import re
import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import HTTPException
from pydantic import validator, EmailStr
from pydantic.main import BaseModel


class AchievementBase(BaseModel):
    description: str
    title: str

    class Config:
        orm_mode = True


class AchievementCreate(AchievementBase):
    pass


class AchievementsUpdate(AchievementBase):
    pass


class AchievementShow(AchievementBase):
    created_at: datetime
    id: uuid.UUID
