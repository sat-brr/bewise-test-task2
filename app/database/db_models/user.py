import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.engine import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    access_token = Column(UUID(as_uuid=True),
                          default=uuid.uuid4)
