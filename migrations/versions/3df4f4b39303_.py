"""empty message

Revision ID: 3df4f4b39303
Revises: 4112b00b9968
Create Date: 2021-05-20 14:36:16.676515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df4f4b39303'
down_revision = '4112b00b9968'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
