"""added-seller-address

Revision ID: 27c2faccf3dd
Revises: 0001_initial
Create Date: 2025-10-04 19:24:19.864277

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "27c2faccf3dd"
down_revision: Union[str, Sequence[str], None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "seller",
        sa.Column("address", sa.String(), nullable=False, server_default="UNKNOWN"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("seller", "address")
