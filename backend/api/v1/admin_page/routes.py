from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from .schemas import (
    AuthUser,
    UserReturnData,
    UserVerifySchema,
)

from .services import AuthService



router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post(
    path='/register',
    response_model=UserReturnData,
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    creds: AuthUser,
    service: Annotated[AuthService, Depends(AuthService)]
) -> UserReturnData:
    return await service.register_admin(creds=creds)