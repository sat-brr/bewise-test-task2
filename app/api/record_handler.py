import uuid

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Request,
                     UploadFile)
from fastapi.responses import Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.actions.record_utils import write_record_to_db
from app.api.actions.user_utils import token_validation
from app.api.schemas import ShowDownloadUrl
from app.database.dao import RecordDAO
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
    user_id: int = Form(...),
    access_token: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
) -> ShowDownloadUrl:

    await token_validation(session, user_id, access_token)

    try:

        record = await write_record_to_db(session, user_id, file)

        url = (f"{request.base_url}record?"
               f"id={record.record_id}&user={record.user_id}")

        return ShowDownloadUrl(download_url=url)

    except SQLAlchemyError as err:
        raise HTTPException(status_code=503, detail=f"Databse error: {err}")
