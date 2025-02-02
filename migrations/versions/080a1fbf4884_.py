"""empty message

Revision ID: 080a1fbf4884
Revises: 1fbe5dcf2b5d
Create Date: 2021-05-18 12:36:16.579967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '080a1fbf4884'
down_revision = '1fbe5dcf2b5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('name', sa.String(), nullable=True))
    op.add_column('customers', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('customers', sa.Column('postal_code', sa.Integer(), nullable=True))
    op.add_column('customers', sa.Column('videos_checked_out_count', sa.Integer(), nullable=True))
    op.drop_column('customers', 'newCustomerName')
    op.drop_column('customers', 'newCustomerVideosCheckedOut')
    op.drop_column('customers', 'newCustomerPhone')
    op.drop_column('customers', 'newCustomerPostalCode')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('newCustomerPostalCode', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('customers', sa.Column('newCustomerPhone', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('customers', sa.Column('newCustomerVideosCheckedOut', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('customers', sa.Column('newCustomerName', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('customers', 'videos_checked_out_count')
    op.drop_column('customers', 'postal_code')
    op.drop_column('customers', 'phone')
    op.drop_column('customers', 'name')
    # ### end Alembic commands ###
