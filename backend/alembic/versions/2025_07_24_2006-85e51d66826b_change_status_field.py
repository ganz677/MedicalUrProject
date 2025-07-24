from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "576be8db6863"
down_revision = "4cd687ef8f4e"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1) создаём тип ENUM
    status_enum = postgresql.ENUM(
        "new", "confirmed", "canceled",
        name="appointment_status",
        create_type=True,
    )
    status_enum.create(op.get_bind(), checkfirst=True)

    # 2) меняем тип столбца, указывая USING
    op.alter_column(
        "appointments",
        "status",
        existing_type=sa.VARCHAR(length=50),
        type_=status_enum,
        existing_nullable=False,
        existing_comment="Статус записи",
        postgresql_using="status::appointment_status",
    )


def downgrade() -> None:
    # 1) возвращаем назад на VARCHAR
    op.alter_column(
        "appointments",
        "status",
        existing_type=postgresql.ENUM(
            "new", "confirmed", "canceled",
            name="appointment_status",
        ),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
        existing_comment="Статус записи",
    )
    # 2) удаляем ENUM-тип
    status_enum = postgresql.ENUM(
        "new", "confirmed", "canceled",
        name="appointment_status",
    )
    status_enum.drop(op.get_bind(), checkfirst=True)
