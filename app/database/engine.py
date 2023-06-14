from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app import settings

Base = declarative_base()

engine = create_async_engine(settings.DB_URL, echo=True)

async_db_session = sessionmaker(bind=engine,
                                expire_on_commit=False,
                                class_=AsyncSession)


async def get_session() -> AsyncSession:
    try:
        session: AsyncSession = async_db_session()
        yield session
    finally:
        await session.close()
