"""create workflow_steps table

Revision ID: 5dfcbb882058
Revises: 24a7971cd290
Create Date: 2026-10-01 06:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dfcbb882058'
down_revision: Union[str, Sequence[str], None] = '24a7971cd290'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('workflow_steps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('system_instructions', sa.String(), nullable=False),
        sa.Column('response_schema', sa.String(), nullable=True),
        sa.Column('skills_paths', sa.String(), nullable=True),
        sa.CheckConstraint('"order" > 0', name='check_workflow_steps_order_positive'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_workflow_steps_id'), 'workflow_steps', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_workflow_steps_id'), table_name='workflow_steps')
    op.drop_table('workflow_steps')
