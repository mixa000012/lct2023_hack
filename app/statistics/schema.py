import uuid

from pydantic.main import BaseModel


class StatisticsBase(BaseModel):
    article_id: uuid.UUID
    time_to_complete: str
    user_id: uuid.UUID
    right_answers: int
    is_deadline: bool

    class Config:
        orm_mode = True


class StatisticsCreate(StatisticsBase):
    pass


class StatisticsUpdate(StatisticsBase):
    pass
