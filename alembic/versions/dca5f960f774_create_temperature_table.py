"""create temperature table

Revision ID: dca5f960f774
Revises: 4e39a75cf216
Create Date: 2023-09-08 20:18:12.374461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dca5f960f774'
down_revision: Union[str, None] = '4e39a75cf216'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
