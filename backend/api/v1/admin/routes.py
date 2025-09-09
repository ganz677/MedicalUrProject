from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)

from .schemas import (
    AuthUser,
    CreateUser,
    UserReturnData,
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


@router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
)
async def login(
    admin: CreateUser,
    service: Annotated[AuthService, Depends(AuthService)],
):
    return await service.login_admin(admin=admin)