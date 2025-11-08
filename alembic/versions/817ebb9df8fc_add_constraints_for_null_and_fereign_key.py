"""add constraints for null and foreign key

Revision ID: 817ebb9df8fc
Revises: 639f9f03f6db
Create Date: 2025-11-08 11:31:00.860769

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "817ebb9df8fc"
down_revision: Union[str, Sequence[str], None] = "639f9f03f6db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Alter City table
    with op.batch_alter_table("City", schema=None) as batch_op:
        batch_op.alter_column("name", existing_type=sa.VARCHAR(), nullable=False)

    # Alter Temperature table
    with op.batch_alter_table("Temperature", schema=None) as batch_op:
        batch_op.alter_column("city_id", existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column("date_time", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("temperature", existing_type=sa.FLOAT(), nullable=False)
        batch_op.create_foreign_key(
            "fk_temperature_city", "City", ["city_id"], ["id"], ondelete="CASCADE"
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("Temperature", schema=None) as batch_op:
        batch_op.drop_constraint("fk_temperature_city", type_="foreignkey")
        batch_op.alter_column("temperature", existing_type=sa.FLOAT(), nullable=True)
        batch_op.alter_column("date_time", existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column("city_id", existing_type=sa.INTEGER(), nullable=True)

    # Revert City table
    with op.batch_alter_table("City", schema=None) as batch_op:
        batch_op.alter_column("name", existing_type=sa.VARCHAR(), nullable=True)
