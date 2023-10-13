"""New migration

Revision ID: 9ab3748fd89b
Revises: f468f2ba86dd
Create Date: 2023-10-03 18:21:48.275089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ab3748fd89b'
down_revision: Union[str, None] = 'f468f2ba86dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
