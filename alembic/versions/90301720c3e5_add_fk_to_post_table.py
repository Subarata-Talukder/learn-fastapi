"""add FK to post table

Revision ID: 90301720c3e5
Revises: 32a224c42b18
Create Date: 2022-02-11 17:30:02.115849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90301720c3e5'
down_revision = '32a224c42b18'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
