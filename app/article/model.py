from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import DateTime
import uuid
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db.base_class import Base


class Article(Base):
    __tablename__ = 'article'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    content = Column(String)
    created_by = Column(UUID, ForeignKey('users.user_id'))
    created_at = Column(DateTime(timezone=True), default=func.now())
    expire_at = Column(DateTime(timezone=True))
    questions = relationship("Question", backref="article", lazy='noload')