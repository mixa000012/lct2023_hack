from datetime import datetime
from app.questions.schema import QuestionBase
import uuid
from typing import List

from pydantic.main import BaseModel


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
