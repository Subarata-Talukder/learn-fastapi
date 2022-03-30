"""create content

Revision ID: 1723504581b2
Revises: 1530b2cfcfe5
Create Date: 2022-02-11 17:12:08.671157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1723504581b2'
down_revision = '1530b2cfcfe5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
