import os

import aiofiles
from fastapi import UploadFile
from pydub import AudioSegment
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dao import RecordDAO
from app.database.db_models.record import Record


async def format_wav_to_mp3(file: UploadFile) -> bytes:
    record = AudioSegment.from_file(file.file, format="wav")
    async with aiofiles.tempfile.TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(tmp_dir, 'tmp_file.mp3')
        record.export(file_path, format="mp3")
        async with aiofiles.open(file_path, mode="rb") as file:
            return await file.read()


async def write_record_to_db(
    session: AsyncSession, user_id: int, file: UploadFile
) -> Record:

    new_name = file.filename.split('.')[0] + '.mp3'
    content = await format_wav_to_mp3(file)
    return await RecordDAO.create_record(
        session, title=new_name, user_id=user_id, content=content
    )
