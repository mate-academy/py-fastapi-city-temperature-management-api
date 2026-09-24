"""delete unique from add.info city model

Revision ID: 6ac8bda4e997
Revises: 1634a0ae8eae
Create Date: 2026-09-25 02:25:28.700333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ac8bda4e997'
down_revision: Union[str, Sequence[str], None] = '1634a0ae8eae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

naming_convention = {"uq": "uq_%(table_name)s_%(column_0_name)s"}


def upgrade() -> None:
    """Remove the unique constraint from city.additional_info."""
    with op.batch_alter_table("city", naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint("uq_city_additional_info", type_="unique")


def downgrade() -> None:
    """Restore the unique constraint on city.additional_info."""
    with op.batch_alter_table("city", naming_convention=naming_convention) as batch_op:
        batch_op.create_unique_constraint("uq_city_additional_info", ["additional_info"])