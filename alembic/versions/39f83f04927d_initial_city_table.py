"""Initial city table

Revision ID: 39f83f04927d
Revises: 
Create Date: 2023-11-07 18:27:57.755586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "39f83f04927d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "city",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(length=127), nullable=False),
        sa.Column("additional_info", sa.String(length=1023), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    pass
