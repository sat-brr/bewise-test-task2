from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import ShowUser, UserCreate
from app.database.dao import UserDAO
from app.database.engine import get_session

user_router = APIRouter()


@user_router.post("/")
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_session)
) -> ShowUser:

    user_exists = await UserDAO.check_user_exists(session, user.name)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User already exists!")
    try:
        new_usr = await UserDAO.create_user(session, user.name)
        return ShowUser.parse_obj(new_usr.__dict__)
    except SQLAlchemyError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
