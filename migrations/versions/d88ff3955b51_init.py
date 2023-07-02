"""init

Revision ID: d88ff3955b51
Revises: 
Create Date: 2023-07-01 22:28:12.885156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd88ff3955b51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('draft',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pack',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=False)

    op.create_table('deck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('draft_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('deck_name', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['draft_id'], ['draft.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('deck', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_deck_deck_name'), ['deck_name'], unique=False)

    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nrdb_id', sa.Integer(), nullable=True),
    sa.Column('card_name', sa.String(length=128), nullable=True),
    sa.Column('faction', sa.String(length=64), nullable=True),
    sa.Column('card_type', sa.String(length=64), nullable=True),
    sa.Column('agenda_points', sa.Integer(), nullable=True),
    sa.Column('deck_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_card_agenda_points'), ['agenda_points'], unique=False)
        batch_op.create_index(batch_op.f('ix_card_card_name'), ['card_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_card_card_type'), ['card_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_card_faction'), ['faction'], unique=False)
        batch_op.create_index(batch_op.f('ix_card_nrdb_id'), ['nrdb_id'], unique=True)

    op.create_table('pack_card',
    sa.Column('pack_id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
    sa.ForeignKeyConstraint(['pack_id'], ['pack.id'], ),
    sa.PrimaryKeyConstraint('pack_id', 'card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pack_card')
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_card_nrdb_id'))
        batch_op.drop_index(batch_op.f('ix_card_faction'))
        batch_op.drop_index(batch_op.f('ix_card_card_type'))
        batch_op.drop_index(batch_op.f('ix_card_card_name'))
        batch_op.drop_index(batch_op.f('ix_card_agenda_points'))

    op.drop_table('card')
    with op.batch_alter_table('deck', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_deck_deck_name'))

    op.drop_table('deck')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('pack')
    op.drop_table('draft')
    # ### end Alembic commands ###
