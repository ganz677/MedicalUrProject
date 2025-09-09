# backend/api/v1/appointments/managers.py
from uuid import UUID
from typing import TYPE_CHECKING, Annotated, List, Dict, Any
import re

from sqlalchemy import select, insert, and_
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status

from backend.core.models import db_helper, Appointment
from backend.api.v1.appointments.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentDB,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def _normalize_phone(raw: str) -> str:
    """Оставляем + и цифры, прибираем пробелы/скобки/дефисы. 8XXXXXXXXXX -> +7XXXXXXXXXX."""
    s = re.sub(r"[^\d+]", "", raw or "")
    if s.startswith("8") and len(s) == 11:
        s = "+7" + s[1:]
    if not s.startswith("+") and s.isdigit():
        s = "+" + s
    return s


def _filter_to_model_columns(model, data: Dict[str, Any]) -> Dict[str, Any]:
    """Только реальные колонки таблицы, без None — чтобы не ловить NOT NULL."""
    cols = set(model.__table__.columns.keys())
    return {k: v for k, v in data.items() if k in cols and v is not None}


class AppointmentManager:
    def __init__(self, db: Annotated['AsyncSession', Depends(db_helper.session_getter)]) -> None:
        self.db = db
        self.model = Appointment

    async def create_appointment(self, appointment: AppointmentCreate) -> AppointmentResponse:
        # 1) нормализуем и готовим данные
        payload = appointment.model_dump()
        payload["phone_number"] = _normalize_phone(payload.get("phone_number", ""))

        # 2) проверка дубля (ФИО + телефон)
        existing_q = select(self.model).where(
            and_(
                self.model.first_name == payload.get("first_name"),
                self.model.last_name == payload.get("last_name"),
                self.model.phone_number == payload.get("phone_number"),
            )
        )
        existing = await self.db.execute(existing_q)
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такая запись уже существует"
            )

        # 3) фильтруем под реальные колонки; status/consent имеют дефолты на БД — можно не указывать
        insert_data = _filter_to_model_columns(self.model, payload)

        try:
            result = await self.db.execute(
                insert(self.model).values(**insert_data).returning(self.model)
            )
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            msg = str(getattr(e, "orig", e)).lower()

            if "unique" in msg or "duplicate" in msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такая запись уже существует (уникальное ограничение)"
                )
            if "not null" in msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Заполнены не все обязательные поля (NOT NULL)"
                )
            if "enum" in msg and "invalid" in msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Некорректное значение для поля-ENUM (status)"
                )

            # общий случай — отдать первопричину
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Не удалось создать запись: {msg}"
            )

        created = result.scalar_one()
        return AppointmentResponse(
            success=True,
            message="Запись успешно создана",
            appointment=AppointmentDB.model_validate(created, from_attributes=True)
        )

    async def get_appointments(self) -> List[AppointmentDB]:
        result = await self.db.execute(select(self.model))
        rows = result.scalars().all()
        return [AppointmentDB.model_validate(obj, from_attributes=True) for obj in rows]

    async def get_single_appointment(self, id: UUID) -> AppointmentDB:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one_or_none()
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return AppointmentDB.model_validate(obj, from_attributes=True)
