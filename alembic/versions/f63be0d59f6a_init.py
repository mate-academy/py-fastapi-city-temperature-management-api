from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f63be0d59f6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("additional_info", sa.String(length=255), nullable=True)
    )

    op.create_table(
        "temperatures",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("city_id", sa.Integer, sa.ForeignKey("cities.id"), nullable=False),
        sa.Column("temperature", sa.Float, nullable=False),
        sa.Column("date_time", sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("temperatures")
    op.drop_table("cities")
