"""Increase transaction_no length

Revision ID: 39badac88df5
Revises: f632b07fe41b
Create Date: 2025-09-18 14:29:36.715192
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39badac88df5'
down_revision = 'f632b07fe41b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'transactions',               # table name
        'transaction_no',             # column name
        existing_type=sa.VARCHAR(length=16),  # old length
        type_=sa.VARCHAR(length=50),          # new length
        existing_nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'transactions',
        'transaction_no',
        existing_type=sa.VARCHAR(length=50),
        type_=sa.VARCHAR(length=16),
        existing_nullable=False
    )
