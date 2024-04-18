"""Description of changes

Revision ID: ff1d1c1fde35
Revises: 64d3d30e8b68
Create Date: 2024-04-16 12:15:40.020202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff1d1c1fde35'
down_revision: Union[str, None] = '64d3d30e8b68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'city',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('additional_info', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_city_name', 'name'),
    )
    op.create_table(
        'temperature',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date_time', sa.DateTime(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('city_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_temperature_date_time', 'date_time'),
    )


def downgrade() -> None:

    op.drop_table('city')
    op.drop_table('temperature')
