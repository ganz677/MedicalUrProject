from enum import Enum as PyEnum

from sqlalchemy import (
    String,
    Boolean,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy.dialects.postgresql import ENUM as PGEnum


from .base import Base
from .mixins.id_mixin import IDMixin
from .mixins.timestamp_mixin import TimeStampMixin

class AppointmentStatus(str, PyEnum):
    new = 'new'
    confirmed = 'confirmed'
    canceled = 'canceled'

class Appointment(IDMixin, TimeStampMixin, Base):
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='Имя пациента'
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='Фамилия пациента'
    )
    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment='Номер телефона пациента'
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment='Email пациента'
    )
    age: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment='Возрастная группа'
    )
    preferred_time: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        comment='Предпочтительное время'
    ) 
    message: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        comment='Дополнительное сообщение'
    )
    privacy_consent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment='Согласие на обработку'
    )
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, name='{self.first_name} {self.last_name}', phone='{self.phone_number}')>"
