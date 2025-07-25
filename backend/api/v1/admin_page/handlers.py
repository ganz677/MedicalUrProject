import datetime
import uuid

import bcrypt
import jwt

from fastapi import (
    HTTPException,
    status
)

from core.settings import settings

from .named_tuples import CreateTokenTuple


class AuthHandler:
    def __init__(self):
        self.private_key: str = settings.auth_jwt.private_key_path.read_text()
        self.public_key: str = settings.auth_jwt.public_key_path.read_text()
        self.algorithm: str = settings.auth_jwt.algorithm
        self.expire_seconds: int = settings.auth_jwt.access_token_lifetime_seconds

    def hash_password(
        self,
        password: str,
    ) -> str:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode('utf-8')


    def verify_password(
        self,
        raw_password: str,
        hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())

    async def create_access_token(
        self,
        user_id: uuid.UUID,
    ) -> CreateTokenTuple:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=settings.auth_jwt.access_token_lifetime_seconds)
        session_id = str(uuid.uuid4())

        payload = {
            'exp': expire,
            'session_id': session_id,
            'user_id': str(user_id),
        }

        encoded_jwt = jwt.encode(payload=payload, key=self.private_key, algorithm=self.algorithm)

        return CreateTokenTuple(encoded_jwt=encoded_jwt, session_id=session_id)


    async def decode_access_token(
        self,
        token: str | bytes,
    ) -> dict:
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self.public_key,
                algorithms=[self.algorithm],
            )
            return decoded
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token has Expired'
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )