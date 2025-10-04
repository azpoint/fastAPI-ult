from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.database.models import ShipmentStatus  # import your Python enum

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "seller",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
    )

    op.create_table(
        "shipment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("destination", sa.String(), nullable=False),
        sa.Column(
            "status", sa.Enum(ShipmentStatus, name="shipmentstatus"), nullable=False
        ),
        sa.Column("estimated_delivery", sa.DateTime(), nullable=False),
        sa.Column(
            "seller_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("seller.id"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("shipment")
    op.drop_table("seller")
