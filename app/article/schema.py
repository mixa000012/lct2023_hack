import uuid
from datetime import datetime
from typing import List

from pydantic.main import BaseModel

from app.questions.schema import QuestionBase


class ArticleBase(BaseModel):
    name: str
    expire_at: datetime
    content: str

    class Config:
        orm_mode = True


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class ArticleShow(ArticleBase):
    created_by: uuid.UUID
    created_at: datetime
    id: uuid.UUID
    questions: List[QuestionBase]


class Deadline(BaseModel):
    user_id: uuid.UUID
    article_id: uuid.UUID
    expire_at: datetime | None
    articles: ArticleShow

    class Config:
        orm_mode = True
