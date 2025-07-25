from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse

from itsdangerous import (
    BadSignature,
    URLSafeTimedSerializer,
)

from core.settings import settings
from .managers import AuthManager
from .handlers import AuthHandler
from .schemas import (
    AuthUser,
    CreateUser,
    UserReturnData,
    UserVerifySchema,
)


class AuthService:
    def __init__(
        self,
        manager: Annotated[AuthManager, Depends(AuthManager)],
        handler: Annotated[AuthHandler, Depends(AuthHandler)],
    ):
        pass