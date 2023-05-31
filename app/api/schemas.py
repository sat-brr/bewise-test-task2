import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, validator

PATTERN = re.compile(r"^[а-яА-Яa-zA-Z]+$")


class UserCreate(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, value):
        if not PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Name must contains only letters."
            )
        return value


class ShowUser(BaseModel):
    id: int
    access_token: uuid.UUID


class ShowDownloadUrl(BaseModel):
    download_url: str
