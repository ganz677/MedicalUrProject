import bcrypt

from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status
)

from .managers import AuthManager
from .schemas import (
    AuthUser,
    CreateUser,
    UserReturnData,
)


class AuthService:
    def __init__(self, manager: Annotated[AuthManager, Depends(AuthManager)]):
        self.manager = manager

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())

    async def register_admin(self, creds: AuthUser) -> UserReturnData:
        hashed_password = self.hash_password(creds.password)
        new_admin = CreateUser(login=creds.login, hashed_password=hashed_password)
        return await self.manager.create_admin(new_admin)

    async def login_admin(self, admin: AuthUser) -> UserReturnData:
        db_admin = await self.manager.get_admin_by_login(admin.login)
        if not db_admin:
            raise HTTPException(status_code=401, detail="Админ с таким логином не найден")

        if not self.verify_password(admin.password, db_admin.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        return UserReturnData(**db_admin.__dict__)