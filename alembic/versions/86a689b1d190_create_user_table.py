"""create user table

Revision ID: 86a689b1d190
Revises: df87b30a60a8
Create Date: 2024-05-10 22:48:53.635275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86a689b1d190'
down_revision: Union[str, None] = 'df87b30a60a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
