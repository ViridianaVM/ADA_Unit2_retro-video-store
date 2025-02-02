"""empty message

Revision ID: 7d4c6c4467b8
Revises: 560ee2893603
Create Date: 2021-05-19 00:10:53.342017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d4c6c4467b8'
down_revision = '560ee2893603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('videos_checked_out_count', sa.Integer(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('videos',
    sa.Column('video_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('total_inventory', sa.Integer(), nullable=True),
    sa.Column('available_inventory', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('video_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('videos')
    op.drop_table('customers')
    # ### end Alembic commands ###
