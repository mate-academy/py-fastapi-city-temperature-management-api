"""initial migration

Revision ID: 7aa9c0c0c441
Revises: fa4b9095004c
Create Date: 2025-02-15 11:07:48.681158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aa9c0c0c441'
down_revision: Union[str, None] = 'fa4b9095004c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
