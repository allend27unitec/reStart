"""create car table

Revision ID: f41178415306
Revises: ad72434b4e5e
Create Date: 2024-05-26 00:19:07.249629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.base_model import OrmBase
from models.owner_model import Car


# revision identifiers, used by Alembic.
revision: str = 'f41178415306'
down_revision: Union[str, None] = 'ad72434b4e5e'
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
