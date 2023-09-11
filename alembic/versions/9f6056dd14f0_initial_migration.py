"""empty message
Revision ID: 9f6056dd14f0
Revises: 1c5934e6e321
Create Date: 2023-09-11 15:01:27.775856
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '9f6056dd14f0'
down_revision: Union[str, None] = '1c5934e6e321'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('temperatures',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.Column('date_time', sa.DateTime(), nullable=True),
                    sa.Column('temperature', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(
        op.f('ix_temperatures_id'),
        'temperatures',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_temperatures_id'), table_name='temperatures')
    op.drop_table('temperatures')
