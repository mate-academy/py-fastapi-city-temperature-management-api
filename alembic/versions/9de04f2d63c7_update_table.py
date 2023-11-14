"""update table

Revision ID: 9de04f2d63c7
Revises: 18c3089df670
Create Date: 2023-11-07 19:57:32.196795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9de04f2d63c7'
down_revision: Union[str, None] = '18c3089df670'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
