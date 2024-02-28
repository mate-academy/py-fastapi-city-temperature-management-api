"""CityTemperature migration

Revision ID: 6a0ac87c5c7c
Revises: 7f15ff3010b2
Create Date: 2024-02-27 14:28:57.694689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a0ac87c5c7c'
down_revision: Union[str, None] = '7f15ff3010b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temperature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('temperature', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_temperature_id'), 'temperature', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_temperature_id'), table_name='temperature')
    op.drop_table('temperature')
    # ### end Alembic commands ###
