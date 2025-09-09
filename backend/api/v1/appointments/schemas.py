from uuid import UUID

import re
from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict
)


from pydantic import field_validator

class AppointmentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = None
    age: str
    phone_number: str
    message: str | None = None
    privacy_consent: bool = True

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        digits = "".join(ch for ch in v if ch.isdigit())
        if digits.startswith("8"):
            digits = "7" + digits[1:]
        if not digits.startswith("7"):
            digits = "7" + digits
        e164 = "+" + digits
        if len(digits) < 11 or len(digits) > 15:
            raise ValueError("Некорректный номер телефона")
        return e164


    
    
    
class AppointmentCreate(AppointmentBase):
    '''Схема для создания записи на прием'''
    
    
class AppointmentDB(AppointmentBase):
    """Схема записи из базы данных"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
        
        

class AppointmentResponse(BaseModel):
    """Схема ответа при создании записи"""
    success: bool
    appointment: AppointmentDB
    message: str
    
