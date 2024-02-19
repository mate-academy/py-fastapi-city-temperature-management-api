"""migrate temperature

Revision ID: b1401529be79
Revises: 71247f30e0af
Create Date: 2024-02-19 17:06:28.766567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1401529be79'
down_revision: Union[str, None] = '71247f30e0af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temperatures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('temperature', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_temperatures_id'), 'temperatures', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_temperatures_id'), table_name='temperatures')
    op.drop_table('temperatures')
    # ### end Alembic commands ###
