"""adding cardpool field

Revision ID: c16e8086de22
Revises: d9bcd512fc4e
Create Date: 2023-07-03 08:22:30.397732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c16e8086de22'
down_revision = 'd9bcd512fc4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cardpool', sa.String(length=64), nullable=True))
        batch_op.create_index(batch_op.f('ix_card_cardpool'), ['cardpool'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_card_cardpool'))
        batch_op.drop_column('cardpool')

    # ### end Alembic commands ###