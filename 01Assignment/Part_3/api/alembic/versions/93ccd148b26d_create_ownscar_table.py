"""create ownscar table

Revision ID: 93ccd148b26d
Revises: f41178415306
Create Date: 2024-05-26 00:19:30.858919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.base_model import OrmBase
from models.owner_model import OwnsCar


# revision identifiers, used by Alembic.
revision: str = '93ccd148b26d'
down_revision: Union[str, None] = 'f41178415306'
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
