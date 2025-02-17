"""initial migration

Revision ID: 2e0096b10327
Revises: 7aa9c0c0c441
Create Date: 2025-02-17 09:03:18.151129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e0096b10327'
down_revision: Union[str, None] = '7aa9c0c0c441'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
