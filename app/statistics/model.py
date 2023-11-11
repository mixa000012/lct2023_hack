import uuid

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.db.base_class import Base


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID, ForeignKey('article.id'))
    time_to_complete = Column(String)
    user_id = Column(UUID, ForeignKey("users.user_id"))
    right_answers = Column(Integer)
    is_deadline = Column(Boolean)
