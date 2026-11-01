"""fix cascade delete

Revision ID: cfdaf32b1a36
Revises: 7513d87dcadf
Create Date: 2026-11-01 15:26:44.775002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfdaf32b1a36'
down_revision: Union[str, Sequence[str], None] = '7513d87dcadf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


naming_convention = {
    "fk": (
        "fk_%(table_name)s_"
        "%(column_0_name)s_"
        "%(referred_table_name)s"
    ),
}


def upgrade() -> None:
    with op.batch_alter_table(
        "temperature",
        naming_convention=naming_convention,
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_temperature_city_id_cities",
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            "fk_temperature_city_id_cities",
            "cities",
            ["city_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "temperature",
        naming_convention=naming_convention,
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_temperature_city_id_cities",
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            "fk_temperature_city_id_cities",
            "cities",
            ["city_id"],
            ["id"],
        )