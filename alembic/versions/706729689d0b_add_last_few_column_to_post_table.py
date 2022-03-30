"""add last few column to post table

Revision ID: 706729689d0b
Revises: 90301720c3e5
Create Date: 2022-02-11 17:38:59.484230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '706729689d0b'
down_revision = '90301720c3e5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
