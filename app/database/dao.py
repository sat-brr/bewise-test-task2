import uuid

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.record import Record
from app.database.db_models.user import User


class UserDAO(User):

    @classmethod
    async def create_user(
        cls, session: AsyncSession, name: str
    ) -> User | None:

        try:
            new_user = cls(name=name)
            session.add(new_user)
            await session.commit()
            return new_user
        except SQLAlchemyError as err:
            await session.rollback()
            raise err

    @classmethod
    async def check_access_token(
            cls, session: AsyncSession, user_id: int, access_token: uuid.UUID
    ) -> User | None:

        query = select(cls).where(
            and_(cls.id == user_id, cls.access_token == access_token)
        )

        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def check_user_exists(
        cls, session: AsyncSession, name: str
    ) -> User | None:

        query = select(cls).where(cls.name == name)
        result = await session.execute(query)
        return result.scalars().first()


class RecordDAO(Record):

    @classmethod
    async def create_record(cls, session: AsyncSession, **kwargs) -> Record:
        try:
            new_record = cls(**kwargs)
            session.add(new_record)
            await session.commit()
            return new_record
        except SQLAlchemyError as err:
            await session.rollback()
            raise err

    @classmethod
    async def get_record(
        cls: Record, session: AsyncSession, record_id: uuid.UUID, user_id: int
    ) -> Record | None:

        query = select(cls).where(
            and_(cls.record_id == record_id, cls.user_id == user_id))
        result = await session.execute(query)
        return result.scalars().first()
