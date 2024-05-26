"""create employee table

Revision ID: 764a04de7c93
Revises: 440b9b28197f
Create Date: 2024-05-25 22:32:44.031770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.base_model import OrmBase
from models.employee_model import Employee


# revision identifiers, used by Alembic.
revision: str = '764a04de7c93'
down_revision: Union[str, None] = '440b9b28197f'
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

