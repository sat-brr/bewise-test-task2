import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dao import UserDAO


async def token_validation(
    session: AsyncSession, user_id: int, access_token: uuid.UUID
) -> None:

    user = await UserDAO.check_access_token(session, user_id, access_token)
    if not user:
        raise HTTPException(
            status_code=403,
            detail='Forbidden.'
        )
