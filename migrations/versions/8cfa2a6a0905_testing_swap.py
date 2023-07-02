"""testing swap

Revision ID: 8cfa2a6a0905
Revises: d88ff3955b51
Create Date: 2023-07-01 22:30:08.970102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cfa2a6a0905'
down_revision = 'd88ff3955b51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('draft_user',
    sa.Column('draft_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['draft_id'], ['draft.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('draft_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('draft_user')
    # ### end Alembic commands ###