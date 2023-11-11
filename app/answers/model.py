from enum import Enum
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime
import uuid
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.base_class import Base


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_id = Column(UUID, ForeignKey('options.id'))
    user_id = Column(UUID, ForeignKey('users.user_id'))
    is_answered = Column(Boolean, default=False)
