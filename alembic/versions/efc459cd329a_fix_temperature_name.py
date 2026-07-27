"""Fix temperature name

Revision ID: efc459cd329a
Revises: f6f6959e0311
Create Date: 2026-07-25 15:34:43.193812

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "efc459cd329a"
down_revision: Union[str, Sequence[str], None] = "f6f6959e0311"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("cities") as batch_op:
        batch_op.create_unique_constraint(
            "uq_cities_name",
            ["name"],
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("cities") as batch_op:
        batch_op.drop_constraint(
            "uq_cities_name",
            type_="unique",
        )
    # ### end Alembic commands ###
