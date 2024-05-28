"""marking nullable attributes

Revision ID: a3b149164de5
Revises: 764a04de7c93
Create Date: 2024-05-26 15:21:14.572811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.base_model import OrmBase
from models.employee_model import Employee


# revision identifiers, used by Alembic.
revision: str = 'a3b149164de5'
down_revision: Union[str, None] = '764a04de7c93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    bind = op.get_bind()
#    session = sessionmaker(bind=bind)()
    # reflect the database model
    OrmBase.metadata.create_all(bind=bind)

def downgrade() -> None:
    bind = op.get_bind()
    session = sessionmaker(bind=bind)()
    OrmBase.metadata.drop_all(bind=bind)
