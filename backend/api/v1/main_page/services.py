from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
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