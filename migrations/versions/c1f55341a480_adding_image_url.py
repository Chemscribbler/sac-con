"""adding image_url

Revision ID: c1f55341a480
Revises: 8cfa2a6a0905
Create Date: 2023-07-01 23:09:55.786927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f55341a480'
down_revision = '8cfa2a6a0905'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=256), nullable=True))
        batch_op.create_index(batch_op.f('ix_card_image_url'), ['image_url'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_card_image_url'))
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###
