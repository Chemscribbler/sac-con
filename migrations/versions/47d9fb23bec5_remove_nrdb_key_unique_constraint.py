"""remove nrdb key unique constraint

Revision ID: 47d9fb23bec5
Revises: c16e8086de22
Create Date: 2023-07-03 08:27:45.422131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d9fb23bec5'
down_revision = 'c16e8086de22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_index('ix_card_nrdb_id')
        batch_op.create_index(batch_op.f('ix_card_nrdb_id'), ['nrdb_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_card_nrdb_id'))
        batch_op.create_index('ix_card_nrdb_id', ['nrdb_id'], unique=False)

    # ### end Alembic commands ###
