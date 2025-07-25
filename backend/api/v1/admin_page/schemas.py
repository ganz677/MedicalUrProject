import datetime
import uuid

from pydantic import BaseModel


class GetUserByID(BaseModel):
    id: uuid.UUID | str


class GetUserByLogin(BaseModel):
    login: str


class UserVerifySchema(GetUserByID, GetUserByLogin):
    session_id: uuid.UUID | str | None = None


class CreateUser(GetUserByLogin):
    hashed_password: str


class GetUserWithIDAndLogin(GetUserByID, CreateUser):
    pass


class UserReturnData(GetUserByID, GetUserByLogin):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AuthUser(BaseModel):
    login: str
    password: str
