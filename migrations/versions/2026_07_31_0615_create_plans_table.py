"""create plans table

Revision ID: 24a7971cd290
Revises: c4defe6b397d
Create Date: 2026-07-31 06:15:37.208309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24a7971cd290'
down_revision: Union[str, Sequence[str], None] = 'c4defe6b397d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plans_id'), 'plans', ['id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_plans_id'), table_name='plans')
    op.drop_table('plans')
