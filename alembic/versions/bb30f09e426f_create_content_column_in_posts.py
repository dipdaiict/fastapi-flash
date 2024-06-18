"""create content column in posts

Revision ID: bb30f09e426f
Revises: ddfd047b8974
Create Date: 2024-06-18 21:36:51.124375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb30f09e426f'
down_revision: Union[str, None] = 'ddfd047b8974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

