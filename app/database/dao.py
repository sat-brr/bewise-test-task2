import uuid

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.record import Record
from app.database.db_models.user import User


class UserDAO:
    """Объект доступа к данным таблицы users"""
    @classmethod
    async def create_user(
        cls, session: AsyncSession, name: str
    ) -> User | None:

        try:
            new_user = User(name=name)
            session.add(new_user)
            await session.commit()
            return new_user
        except SQLAlchemyError as err:
            await session.rollback()
            raise err

    @classmethod
    async def check_access_token(
            cls, session: AsyncSession,
            user_id: int, access_token: uuid.UUID
    ) -> User | None:

        query = select(User).where(
            and_(User.id == user_id, User.access_token == access_token)
        )

        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def check_user_exists(
        cls, session: AsyncSession, name: str
    ) -> User | None:

        query = select(User).where(User.name == name)
        result = await session.execute(query)
        return result.scalars().first()


class RecordDAO:
    """Объект доступа к данным таблицы records"""
    @classmethod
    async def create_record(
        cls, session: AsyncSession, **kwargs
    ) -> Record:

        try:
            new_record = Record(**kwargs)
            session.add(new_record)
            await session.commit()
            return new_record
        except SQLAlchemyError as err:
            await session.rollback()
            raise err

    @classmethod
    async def get_record(
        cls, session: AsyncSession, record_id: uuid.UUID, user_id: int
    ) -> Record | None:

        query = select(Record).where(
            and_(Record.record_id == record_id, Record.user_id == user_id))
        result = await session.execute(query)
        return result.scalars().first()
