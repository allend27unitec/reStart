"""create owner table

Revision ID: ad72434b4e5e
Revises: 
Create Date: 2024-05-26 00:18:58.482391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.base_model import OrmBase
from models.owner_model import Owner


# revision identifiers, used by Alembic.
revision: str = 'ad72434b4e5e'
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
