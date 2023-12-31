from sqlalchemy import Column, ForeignKey
import uuid
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db.base_class import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID, ForeignKey('article.id'))
    text = Column(String, index=True)
    options = relationship("Option", backref="questions", lazy='noload')


class Option(Base):
    __tablename__ = 'options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String)
    is_correct = Column(Boolean, default=False)
    question_id = Column(UUID, ForeignKey('questions.id'))