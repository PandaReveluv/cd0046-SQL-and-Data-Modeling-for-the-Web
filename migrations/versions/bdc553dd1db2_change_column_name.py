"""change column name

Revision ID: bdc553dd1db2
Revises: 0f13a91f15d6
Create Date: 2024-07-05 12:08:11.117259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdc553dd1db2'
down_revision = '0f13a91f15d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.String(length=500), nullable=True))
        batch_op.drop_column('website_link')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
        batch_op.drop_column('website')

    # ### end Alembic commands ###