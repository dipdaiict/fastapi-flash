"""create remaining columns

Revision ID: c2bb5d0a1609
Revises: 401b42426b67
Create Date: 2024-06-18 21:41:15.022901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2bb5d0a1609'
down_revision: Union[str, None] = '401b42426b67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding the "published" column
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default=sa.text('TRUE'), nullable=False))

    # Adding the "created_at" column
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

    # Adding the "user_id" column with foreign key constraint
    op.add_column('posts', sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))

def downgrade() -> None:
    # Removing the "user_id" column
    op.drop_column('posts', 'user_id')

    # Removing the "created_at" column
    op.drop_column('posts', 'created_at')

    # Removing the "published" column
    op.drop_column('posts', 'published')