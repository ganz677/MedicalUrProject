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
        self.manager = manager
        self.handler = handler 
        self.serializer = URLSafeTimedSerializer(secret_key=settings.front.secret_key)
        
    async def register_admin(
        self,
        creds=AuthUser
    ) -> UserReturnData:
        hashed_password = self.handler.hash_password(creds.password)
        
        new_admin = CreateUser(login=creds.login, hashed_password=hashed_password)
        
        admin_data = await self.manager.create_admin(admin=new_admin)
        
        return admin_data 
        
        
    async def login_admin(
        self,
        admin: AuthUser,
    ):
        exist_admin = await self.manager.get_admin_by_login(login=admin.login)
        
        if exist_admin is None or not self.handler.verify_password(
            raw_password=admin.password,
            hashed_password=exist_admin.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Wrong email or password'
            )

        token, session_id = await self.handler.create_access_token(user_id=exist_admin.id)

        await self.manager.store_access_token(
            token=token,
            user_id=exist_admin.id,
            session_id=session_id,
        )

        response = JSONResponse(
            content={
                'message': 'Successful authorization'
            }
        )
        response.set_cookie(
            key='Authorization',
            value=token,
            httponly=True,
            max_age=settings.auth_jwt.access_token_lifetime_seconds,
        )

        return response