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

from core.models import (
    Admin,
    db_helper,
    RedisHelper
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
    def __init__(
        self,
        db: Annotated['AsyncSession', Depends(db_helper.session_getter)],
        redis: RedisHelper = Depends(RedisHelper),
    ) -> None:
        self.db = db
        self.redis = redis
        self.model = Admin

    async def create_admin(
        self,
        admin: CreateUser,
    ) -> UserReturnData:
        query = insert(self.model).values(**admin.model_dump()).returning(self.model)
        try:
            result = await self.db.execute(query)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Admin already exists'
            )
            
        await self.db.commit()
        
        admin_data = result.scalar_one_or_none()
        return UserReturnData(**admin_data.__dict__)
    
    
    
    async def get_admin_by_login(
        self,
        login: str,
    ):
        pass
    
    async def store_access_token(self, token: str, user_id: uuid.UUID, session_id: str) -> None:
        async with self.redis.client_getter() as client:
            await client.set(f"{user_id}:{session_id}", token)


    async def get_access_token(self, user_id: uuid.UUID | str, session_id: str) -> str | None:
        async with self.redis.client_getter() as client:
            return await client.get(f'{user_id}:{session_id}')


    async def revoke_access_token(self, user_id: uuid.UUID | str, session_id: str) -> str:
        async with self.redis.client_getter() as client:
            await client.delete(f'{user_id}:{session_id}')


    
    