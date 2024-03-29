"""init torrents table

Revision ID: b90fa40e5314
Revises: 
Create Date: 2022-10-15 20:41:22.575554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b90fa40e5314'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('torrents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('announces', sa.Text(), nullable=False, comment='Coma-separated list of announces'),
    sa.Column('info', sa.BLOB(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('status', sa.Enum('active', 'stopped', 'paused', name='loadingstatus'), nullable=False),
    sa.Column('creation_date', sa.String(length=100), nullable=True),
    sa.Column('created_by', sa.String(length=100), nullable=True),
    sa.Column('encoding', sa.String(length=20), nullable=True),
    sa.Column('publisher', sa.String(length=100), nullable=True),
    sa.Column('publisher_url', sa.String(length=100), nullable=True),
    sa.Column('comment', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('torrents')
    # ### end Alembic commands ###
