"""create user table

Revision ID: df87b30a60a8
Revises: 
Create Date: 2024-05-07 20:00:46.932641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df87b30a60a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('username', sa.String(25), nullable=False),
        sa.Column('email', sa.String(25), nullable=False),
        sa.Column('password', sa.String(50), nullable=False),



def downgrade() -> None:
    op.drop_table('users')
