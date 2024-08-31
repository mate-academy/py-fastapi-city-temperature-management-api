"""Initial migration

Revision ID: d4dd3bba223d
Revises: 8f3ff033bbc6
Create Date: 2024-08-30 18:22:33.845966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4dd3bba223d'
down_revision: Union[str, None] = '8f3ff033bbc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
