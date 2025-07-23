from uuid import UUID

from typing import Annotated

from fastapi import (
    Depends,
)


from .managers import AppointmentManager
from .schemas import AppointmentCreate


class AppointmentService:
    def __init__(
        self,
        manager: Annotated['AppointmentManager', Depends(AppointmentManager)]
    ):
        self.manager = manager
        
        
    async def register_new_appointment(self, appointment: AppointmentCreate):
        return await self.manager.create_appointment(appointment=appointment)
    
    async def get_appointments(self):
        return await self.manager.get_appointments()
    
    async def get_appointment_by_id(self, id: UUID):
        return await self.manager.get_single_appointment(id=id)