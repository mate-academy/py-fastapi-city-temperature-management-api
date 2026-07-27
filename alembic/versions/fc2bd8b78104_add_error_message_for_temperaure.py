"""Add error message for temperaure

Revision ID: fc2bd8b78104
Revises: 13f80f58363d
Create Date: 2026-07-26 14:40:28.707257

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fc2bd8b78104"
down_revision: Union[str, Sequence[str], None] = "13f80f58363d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("temperatures") as batch_op:
        batch_op.add_column(
            sa.Column(
                "error_message",
                sa.String(),
                nullable=True,
            )
        )
        batch_op.alter_column(
            "temperature",
            existing_type=sa.Float(),
            nullable=True,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("temperatures") as batch_op:
        batch_op.alter_column(
            "temperature",
            existing_type=sa.Float(),
            nullable=False,
        )
        batch_op.drop_column("error_message")
