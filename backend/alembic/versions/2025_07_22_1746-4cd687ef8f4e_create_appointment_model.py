"""create appointment model

Revision ID: 4cd687ef8f4e
Revises:
Create Date: 2025-07-22 17:46:58.977132

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4cd687ef8f4e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "appointments",
        sa.Column(
            "first_name",
            sa.String(length=100),
            nullable=False,
            comment="Имя пациента",
        ),
        sa.Column(
            "last_name",
            sa.String(length=100),
            nullable=False,
            comment="Фамилия пациента",
        ),
        sa.Column(
            "phone_number",
            sa.String(length=20),
            nullable=False,
            comment="Номер телефона пациента",
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=True,
            comment="Email пациента",
        ),
        sa.Column(
            "age",
            sa.String(length=20),
            nullable=False,
            comment="Возрастная группа",
        ),
        sa.Column(
            "preferred_time",
            sa.String(length=50),
            nullable=True,
            comment="Предпочтительное время",
        ),
        sa.Column(
            "message",
            sa.Text(),
            nullable=True,
            comment="Дополнительное сообщение",
        ),
        sa.Column(
            "privacy_consent",
            sa.Boolean(),
            nullable=False,
            comment="Согласие на обработку",
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            comment="Статус записи",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_appointments")),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("appointments")

