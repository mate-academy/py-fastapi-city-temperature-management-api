"""add temperature table

Revision ID: 4c7977fdd719
Revises: 76eb6686ccf5
Create Date: 2026-11-03 19:06:21.194532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c7977fdd719'
down_revision: Union[str, Sequence[str], None] = '76eb6686ccf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "temperature",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("date_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["city_id"], ["city.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    pass
