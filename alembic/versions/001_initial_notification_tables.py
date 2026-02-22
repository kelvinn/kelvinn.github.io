"""Initial notification tables

Revision ID: 001_initial
Revises:
Create Date: 2026-02-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime, Date

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create notification_sources table
    op.create_table(
        'notification_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_notification_sources_name'), 'notification_sources', ['name'], unique=True)

    # Create notification_history table
    op.create_table(
        'notification_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('notification_date', Date(), nullable=True),
        sa.Column('notification_time', DateTime(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('alert_type', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['notification_sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_history_notification_date'), 'notification_history', ['notification_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_notification_history_notification_date'), table_name='notification_history')
    op.drop_table('notification_history')
    op.drop_index(op.f('ix_notification_sources_name'), table_name='notification_sources')
    op.drop_table('notification_sources')
