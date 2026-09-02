"""Initial migration

Revision ID: 79e86166eb93
Revises: 
Create Date: 2026-09-02 22:59:15.350593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79e86166eb93'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('additional_info', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cities_id'), 'cities', ['id'], unique=False)
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=False)

    op.create_table(
        'temperatures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city_id', sa.Integer(), nullable=True),
        sa.Column('date_time', sa.DateTime(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_temperatures_id'), 'temperatures', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_temperatures_id'), table_name='temperatures')
    op.drop_table('temperatures')

    op.drop_index(op.f('ix_cities_name'), table_name='cities')
    op.drop_index(op.f('ix_cities_id'), table_name='cities')
    op.drop_table('cities')
