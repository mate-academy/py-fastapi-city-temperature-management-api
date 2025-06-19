"""initial migration

Revision ID: 726743ef8249
Revises: 
Create Date: 2023-06-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '726743ef8249'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'city_temperature',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(length=50), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('city_temperature')