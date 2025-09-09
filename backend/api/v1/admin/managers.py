import uuid

from typing import (
    TYPE_CHECKING,
    Annotated
    
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError

from backend.core.models import (
    Admin,
    db_helper,
)
from .schemas import (
    CreateUser,
    GetUserWithIDAndLogin,
    UserReturnData,
    UserVerifySchema,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class AuthManager:
    def __init__(self, db: Annotated['AsyncSession', Depends(db_helper.session_getter)]):
        self.db = db
        self.model = Admin
        
    async def create_admin(self, admin: CreateUser) -> UserReturnData:
        query = insert(self.model).values(**admin.model_dump()).returning(self.model)
        try:
            result = await self.db.execute(query)
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Admin already exists.")

        admin_data = result.scalar_one()
        return UserReturnData(**admin_data.__dict__)

    async def get_admin_by_login(self, login: str):
        query = select(self.model).where(self.model.login == login)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    