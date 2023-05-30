import uuid
from pathlib import Path

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile)
from fastapi.responses import Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.actions.record_utils import write_record_to_db
from app.database.dao import RecordDAO, UserDAO
from app.database.engine import get_session

record_router = APIRouter()


@record_router.get("")
async def get_record(id: uuid.UUID, user: int,
                     session: AsyncSession = Depends(get_session)) -> Response:
    try:
        record = await RecordDAO.get_record(session, id, user)
        if record is None:
            raise HTTPException(status_code=404,
                                detail='Record not found.')
        headers = {
            'Content-Disposition': f'attachment; filename={record.title}'
        }
        return Response(content=record.content,
                        headers=headers,
                        media_type=record.media_type)
    except SQLAlchemyError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@record_router.post("/")
async def create_record(
    request: Request,
    user_id: int,
    access_token: uuid.UUID,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
) -> str:

    if Path(file.filename.lower()).suffix != '.wav':
        raise HTTPException(
            status_code=409, detail="The record must be .wav format!")

    token_valid = await UserDAO.check_access_token(
        session, user_id, access_token
    )
    if token_valid is None:
        raise HTTPException(
            status_code=403,
            detail='Forbidden.'
        )
    try:
        record = await write_record_to_db(session, user_id, file)
        return (f"{request.base_url}record?"
                f"id={record.record_id}&user={record.user_id}")
    except SQLAlchemyError as err:
        raise HTTPException(status_code=503, detail=f"Databse error: {err}")
