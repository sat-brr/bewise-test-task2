import uuid

from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.engine import Base


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    record_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    title = Column(String, nullable=False)
    media_type = Column(String, default="audio/mp3")
    content = Column(LargeBinary)

    user = relationship('User', backref='records')
