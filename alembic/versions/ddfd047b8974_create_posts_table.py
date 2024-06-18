"""Create Posts Table

Revision ID: ddfd047b8974
Revises: 
Create Date: 2024-06-18 14:17:08.243651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddfd047b8974'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:    # To Make Chnage and Create
    # pass
    op.create_table("posts", 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:   # Handle the Rollback
    # pass
    op.drop_table('posts')
