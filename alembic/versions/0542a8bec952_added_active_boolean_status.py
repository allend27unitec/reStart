"""Added active boolean status

Revision ID: 0542a8bec952
Revises: 86a689b1d190
Create Date: 2024-05-12 22:02:46.441840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0542a8bec952'
down_revision: Union[str, None] = '86a689b1d190'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=False))
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=250),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_column('users', 'active')
    # ### end Alembic commands ###
