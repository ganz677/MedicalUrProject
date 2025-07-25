from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    String,
    Text
)

from .base import Base 
from .mixins.timestamp_mixin import TimeStampMixin
from .mixins.id_mixin import IDMixin

class Admin(IDMixin, TimeStampMixin, Base):
    login: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    
    hashed_password: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )