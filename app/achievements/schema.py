import re
import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import HTTPException, UploadFile
from pydantic import validator, EmailStr
from pydantic.main import BaseModel


class AchievementBase(BaseModel):
    description: str
    title: str

    class Config:
        orm_mode = True


class AchievementFile(AchievementBase):
    image: UploadFile


class AchievementCreate(AchievementBase):
    image: str


class AchievementsUpdate(AchievementBase):
    pass


class AchievementShow(AchievementBase):
    created_at: datetime
    id: uuid.UUID
