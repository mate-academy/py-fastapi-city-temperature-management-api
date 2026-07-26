"""Set delete condition for one to many relationship

Revision ID: 4babfd6fba44
Revises: fc2bd8b78104
Create Date: 2026-07-26 14:56:01.043924

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4babfd6fba44"
down_revision: Union[str, Sequence[str], None] = "fc2bd8b78104"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}


def upgrade() -> None:
    with op.batch_alter_table(
        "temperatures",
        naming_convention=naming_convention,
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_temperatures_city_id_cities",
            type_="foreignkey",
        )

        batch_op.create_foreign_key(
            "fk_temperatures_city_id_cities",
            "cities",
            ["city_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "temperatures",
        naming_convention=naming_convention,
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_temperatures_city_id_cities",
            type_="foreignkey",
        )

        batch_op.create_foreign_key(
            "fk_temperatures_city_id_cities",
            "cities",
            ["city_id"],
            ["id"],
        )
