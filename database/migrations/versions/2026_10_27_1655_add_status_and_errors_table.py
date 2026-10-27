"""add status to message_workflow_steps and create message_workflow_step_errors table

Revision ID: 3c7f9e8a1d2b
Revises: 1b3e3b4dd65b
Create Date: 2026-10-27 16:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c7f9e8a1d2b'
down_revision: Union[str, Sequence[str], None] = '1b3e3b4dd65b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'message_workflow_steps',
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending')
    )

    op.create_table(
        'message_workflow_step_errors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message_workflow_step_id', sa.Integer(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=False),
        sa.Column('error_traceback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['message_workflow_step_id'], ['message_workflow_steps.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_workflow_step_errors_id'), 'message_workflow_step_errors', ['id'], unique=False)
    op.create_index(op.f('ix_message_workflow_step_errors_message_workflow_step_id'), 'message_workflow_step_errors', ['message_workflow_step_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_message_workflow_step_errors_message_workflow_step_id'), table_name='message_workflow_step_errors')
    op.drop_index(op.f('ix_message_workflow_step_errors_id'), table_name='message_workflow_step_errors')
    op.drop_table('message_workflow_step_errors')
    op.drop_column('message_workflow_steps', 'status')
