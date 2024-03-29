"""empty message

Revision ID: 21aa82ad0ca6
Revises: d48f3473ab1e
Create Date: 2023-03-02 19:00:32.428550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "21aa82ad0ca6"
down_revision = "d48f3473ab1e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "userroulette",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("roulette_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["roulette_id"],
            ["roulette.id"],
            name=op.f("fk__userroulette__roulette_id__roulette"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__userroulette__user_id__users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__userroulette")),
        sa.UniqueConstraint("id", name=op.f("uq__userroulette__id")),
    )
    op.create_unique_constraint(op.f("uq__roulette__id"), "roulette", ["id"])
    op.create_unique_constraint(op.f("uq__users__id"), "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq__users__id"), "users", type_="unique")
    op.drop_constraint(op.f("uq__roulette__id"), "roulette", type_="unique")
    op.drop_table("userroulette")
    # ### end Alembic commands ###
