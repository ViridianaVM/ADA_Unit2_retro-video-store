"""empty message

Revision ID: 4b03ef7d0902
Revises: d7e7bdc8fb88
Create Date: 2021-05-20 12:08:22.584099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b03ef7d0902'
down_revision = 'd7e7bdc8fb88'
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
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.video_id'], ),
    sa.PrimaryKeyConstraint('id', 'video_id', 'customer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rentals')
    op.drop_table('videos')
    op.drop_table('customers')
    # ### end Alembic commands ###