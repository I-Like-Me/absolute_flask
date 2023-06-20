"""empty message

Revision ID: 9aeff9d251e2
Revises: 4665d66abf4c
Create Date: 2023-06-20 14:16:08.333588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9aeff9d251e2'
down_revision = '4665d66abf4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('basic__viz__data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('Total_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('basic__viz__data', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_basic__viz__data_Total_count'), ['Total_count'], unique=False)
        batch_op.create_index(batch_op.f('ix_basic__viz__data_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basic__viz__data', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_basic__viz__data_timestamp'))
        batch_op.drop_index(batch_op.f('ix_basic__viz__data_Total_count'))

    op.drop_table('basic__viz__data')
    # ### end Alembic commands ###
