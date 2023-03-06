"""empty message

Revision ID: 2be9d1b6cd30
Revises: 21aa82ad0ca6
Create Date: 2023-03-02 19:04:43.213585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2be9d1b6cd30'
down_revision = '21aa82ad0ca6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userroulette', sa.Column('is_winner', sa.BOOLEAN(), nullable=True))
    op.create_unique_constraint(op.f('uq__userroulette__id'), 'userroulette', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq__userroulette__id'), 'userroulette', type_='unique')
    op.drop_column('userroulette', 'is_winner')
    # ### end Alembic commands ###