"""Initial

Revision ID: 5994dcd21488
Revises: 
Create Date: 2024-05-27 21:13:09.847108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5994dcd21488'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('make', sa.String(), nullable=True),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('style', sa.String(), nullable=True),
    sa.Column('year', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__car')),
    sqlite_autoincrement=False
    )
    op.create_table('owner',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__owner')),
    sqlite_autoincrement=False
    )
    op.create_index(op.f('ix__owner__email'), 'owner', ['email'], unique=True)
    op.create_table('ownscar',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('colour', sa.String(length=255), nullable=False),
    sa.Column('vin', sa.String(length=255), nullable=False),
    sa.Column('purchased_dt', sa.Date(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], name=op.f('fk__ownscar__car_id__car')),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.id'], name=op.f('fk__ownscar__owner_id__owner')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__ownscar'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ownscar')
    op.drop_index(op.f('ix__owner__email'), table_name='owner')
    op.drop_table('owner')
    op.drop_table('car')
    # ### end Alembic commands ###
