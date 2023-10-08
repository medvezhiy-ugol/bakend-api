"""empty message

Revision ID: 02db768cfb3c
Revises: 2be9d1b6cd30
Create Date: 2023-08-01 03:50:56.505566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02db768cfb3c'
down_revision = '2be9d1b6cd30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userroulette', sa.Column('user_phone', sa.VARCHAR(length=25), nullable=False))
    op.add_column('userroulette', sa.Column('wallet_id', sa.UUID(), nullable=False))
    op.drop_constraint('fk__userroulette__user_id__users', 'userroulette', type_='foreignkey')
    op.drop_column('userroulette', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userroulette', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk__userroulette__user_id__users', 'userroulette', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('userroulette', 'wallet_id')
    op.drop_column('userroulette', 'user_phone')
    # ### end Alembic commands ###