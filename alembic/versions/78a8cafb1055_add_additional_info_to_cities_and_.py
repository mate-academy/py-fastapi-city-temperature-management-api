"""add additional_info to cities and rename recorded_at to date_time

Revision ID: 78a8cafb1055
Revises: 29b1e4396f8d
Create Date: 2026-01-29 07:58:23.667278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78a8cafb1055'
down_revision: Union[str, Sequence[str], None] = '29b1e4396f8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add column to cities — це SQLite дозволяє
    op.add_column(
        "cities",
        sa.Column("additional_info", sa.String(), nullable=True),
    )

    # rename column in SQLite через batch mode
    with op.batch_alter_table("temperatures") as batch_op:
        batch_op.alter_column(
            "recorded_at",
            new_column_name="date_time",
            existing_type=sa.DateTime(),
            nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("temperatures") as batch_op:
        batch_op.alter_column(
            "date_time",
            new_column_name="recorded_at",
            existing_type=sa.DateTime(),
            nullable=False,
        )

    op.drop_column("cities", "additional_info")
