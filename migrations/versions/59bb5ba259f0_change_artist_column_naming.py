"""change artist column naming

Revision ID: 59bb5ba259f0
Revises: 413cb30da4ed
Create Date: 2024-07-06 10:19:30.071139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59bb5ba259f0'
down_revision = '413cb30da4ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_venue', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=500), nullable=True))
        batch_op.drop_column('is_seeking_venue')
        batch_op.drop_column('seeking_venue_message')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_venue_message', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('is_seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('seeking_venue')

    # ### end Alembic commands ###