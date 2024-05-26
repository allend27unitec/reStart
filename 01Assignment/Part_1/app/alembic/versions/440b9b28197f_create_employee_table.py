"""create employee table

Revision ID: 440b9b28197f
Revises: 
Create Date: 2024-05-25 22:20:54.544990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.base_model import OrmBase
from models.employee_model import Employee


# revision identifiers, used by Alembic.
revision: str = '440b9b28197f'
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
