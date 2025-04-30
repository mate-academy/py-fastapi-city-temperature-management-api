"""add unique contraince field

Revision ID: b61ac35a7a52
Revises: 33ea9f564bbe
Create Date: 2025-04-30 20:58:51.946306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b61ac35a7a52'
down_revision: Union[str, None] = '33ea9f564bbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("temperature", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_city_datetime", ["city_id", "date_time"])

def downgrade():
    with op.batch_alter_table("temperature", schema=None) as batch_op:
        batch_op.drop_constraint("uq_city_datetime", type_="unique")
