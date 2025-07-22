from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from .schemas import (
    AppointmentCreate,
    AppointmentResponse
)

from .services import AppointmentService


router = APIRouter(
    prefix='/appointments',
    tags=['Appointment']
)


@router.post(
    path="/create",
    response_model=AppointmentResponse,
)
async def accept_appointment(
    appointment: AppointmentCreate,
    service: Annotated['AppointmentService', Depends(AppointmentService)]
) -> AppointmentResponse:
    '''Создание записи на прием'''
    return await service.register_new_appointment(appointment=appointment)