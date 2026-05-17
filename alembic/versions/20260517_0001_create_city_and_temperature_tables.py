from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260517_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("additional_info", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cities_id"), "cities", ["id"], unique=False)
    op.create_index(op.f("ix_cities_name"), "cities", ["name"], unique=False)

    op.create_table(
        "temperatures",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("date_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_temperatures_city_id"), "temperatures", ["city_id"], unique=False)
    op.create_index(op.f("ix_temperatures_id"), "temperatures", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_temperatures_id"), table_name="temperatures")
    op.drop_index(op.f("ix_temperatures_city_id"), table_name="temperatures")
    op.drop_table("temperatures")

    op.drop_index(op.f("ix_cities_name"), table_name="cities")
    op.drop_index(op.f("ix_cities_id"), table_name="cities")
    op.drop_table("cities")
