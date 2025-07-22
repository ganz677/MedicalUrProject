from uuid import UUID

import re
from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)


class AppointmentBase(BaseModel):
    '''Базовая модель для дальнейшего унаследования'''
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[EmailStr] = None
    age: str
    preferred_time: Optional[str] = None
    message: Optional[str] = None
    privacy_consent: bool
    
    class Config:
        str_strip_whitespace = True
    
    
    
class AppointmentCreate(AppointmentBase):
    '''Схема для создания записи на прием'''
    
    @field_validator('first_name', 'last_name')
    def validate_names(cls, v: str) -> str:
        if not v or len(v.strip()) < 1:
            raise ValueError('Имя и фамилия обязательны для заполнения')
        return v.strip()
    
    
    @field_validator('phone_number')
    def validate_phone_number(cls, v: str) -> str:
        if not v or len(v.strip()) < 1:
            raise ValueError('Телефон обязателен для заполнения')
        phone_pattern = r'^\+?\d[\d\s\-\(\)]{7,}$'
        if not re.fullmatch(phone_pattern, v.strip()):
            raise ValueError('Некорректный формат телефона')
        return v.strip()
    
    
    @field_validator('age')
    def validate_age(cls, v: str) -> str:
        if not v or len(v.strip()) < 1:
            raise ValueError('Возраст обязателен для выбора')
        return v.strip()
    
    @field_validator('privacy_consent')
    def validate_privacy_consent(cls, v):
        if not v:
            raise ValueError('Необходимо согласие на обработку данных')
        return v
    
    
    
class AppointmentDB(AppointmentBase):
    """Схема записи из базы данных"""
    id: UUID
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        
        

class AppointmentResponse(BaseModel):
    """Схема ответа при создании записи"""
    success: bool
    appointment: AppointmentDB
    message: str