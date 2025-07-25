from uuid import UUID

from typing import (
    TYPE_CHECKING,
    Annotated,
    List
)

from sqlalchemy import (
    select,
    insert,
)

from sqlalchemy.exc import IntegrityError

from fastapi import (
    Depends,
    status,
    HTTPException,
)

from core.models import (
    db_helper,
    Appointment
)


from api.v1.main_page.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentDB,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class AppointmentManager:
    def __init__(self, db: Annotated['AsyncSession', Depends(db_helper.session_getter)]) -> None:
        self.db = db
        self.model = Appointment
        
        
    async def create_appointment(self, appointment: AppointmentCreate) -> AppointmentResponse:
        
        
        existing = await self.db.execute(
            select(self.model).where(
                self.model.phone_number == appointment.phone_number,
                self.model.first_name == appointment.first_name,
                self.model.last_name == appointment.last_name,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(400, "Запись уже существует")
        
        query = insert(self.model).values(**appointment.model_dump()).returning(self.model)
        try:
            result = await self.db.execute(query)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Appointment already exist'
            )
        
        await self.db.commit()
        appointment_data = result.scalar_one()
        
        return AppointmentResponse(
            success=True,
            message='Запись успешно создана',
            appointment=AppointmentDB.model_validate(appointment_data)
        ) 
        
        
    async def get_appointments(self) -> List[AppointmentDB]:
        query = select(self.model)
        try:
            result = await self.db.execute(query)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Cant get any appointment'
            )
        
        appointments = result.scalars().all()
        
        return [AppointmentDB.model_validate(obj) for obj in appointments]
    
    
    async def get_single_appointment(
        self,
        id: UUID,
    ) -> AppointmentDB:
        query = select(self.model).where(self.model.id == id)

        try:
            result = await self.db.execute(query)
            appointment = result.scalar_one_or_none()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request (integrity error)"
            )

        if appointment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )

        return AppointmentDB.model_validate(appointment, from_attributes=True)
            