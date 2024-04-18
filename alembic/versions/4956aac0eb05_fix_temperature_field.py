"""fix temperature field

Revision ID: 4956aac0eb05
Revises: ff1d1c1fde35
Create Date: 2024-04-17 11:58:46.897905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4956aac0eb05'
down_revision: Union[str, None] = 'ff1d1c1fde35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
