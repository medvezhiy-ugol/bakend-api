"""empty message

Revision ID: ef00f2dbcc5c
Revises: 02db768cfb3c
Create Date: 2023-08-03 18:06:20.300089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef00f2dbcc5c'
down_revision = '02db768cfb3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userroulette', sa.Column('organization_id', sa.UUID(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userroulette', 'organization_id')
    # ### end Alembic commands ###
