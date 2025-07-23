from uuid import UUID

from typing import (
    Annotated,
    List
)

from fastapi import (
    APIRouter,
    Depends,
)

from .schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentDB
)

from .services import AppointmentService


router = APIRouter(
    prefix='/appointments',
    tags=['Appointment'],
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


@router.get(
    path='/all',
    response_model=List[AppointmentDB],
)
async def get_appointments(
    service: Annotated['AppointmentService', Depends(AppointmentService)]
):
    return await service.get_appointments()


@router.get(
    path='/{id}',
    response_model=AppointmentDB,
)
async def get_appointment_by_id(
    id: UUID,
    service: Annotated['AppointmentService', Depends(AppointmentService)]
):
    return await service.get_appointment_by_id(id=id)