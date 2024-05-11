"""create user table

Revision ID: df87b30a60a8
Revises: 
Create Date: 2024-05-07 20:00:46.932641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.schema import Base
from orm.user_model import User
from orm.base_model import OrmBase


# revision identifiers, used by Alembic.
revision: str = 'df87b30a60a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = sessionmaker(bind=bind)()
    # reflect the database model
    OrmBase.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    session = sessionmaker(bind=bind)()
    OrmBase.metadata.drop_all(bind=bind)
