from typing import (
    TYPE_CHECKING,
    Annotated
)

from sqlalchemy import (
    select,
    insert,
    update
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
    AppointmentDB
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class AppointmentManager:
    def __init__(self, db: Annotated['AsyncSession', Depends(db_helper.session_getter)]) -> None:
        self.db = db
        self.model = Appointment
        
        
    async def create_appointment(self, appointment: AppointmentCreate) -> AppointmentResponse:
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
        