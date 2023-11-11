import uuid
from typing import List

import re
from pydantic.main import BaseModel


class OptionSchema(BaseModel):
    text: str


class OptionCreate(OptionSchema):
    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str
    options: List[OptionCreate]
    article_id: uuid.UUID

    class Config:
        orm_mode = True


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass
