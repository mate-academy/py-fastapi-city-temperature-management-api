"""Create city and temperature tables

Revision ID: 0107e8f3a77c
Revises: 
Create Date: 2026-11-03 17:32:09.100644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0107e8f3a77c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "temperature",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("date_time", sa.DateTime(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["city_id"], ["city.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("temperature")
