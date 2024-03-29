"""01_initial-db

Revision ID: bd93d943e332
Revises: 
Create Date: 2022-12-16 14:49:12.394662

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'bd93d943e332'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urlinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.String(length=50), nullable=True),
    sa.Column('long_url', sa.String(length=200), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('long_url'),
    sa.UniqueConstraint('url_id')
    )
    op.create_table('redirect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('person_info', sa.String(length=200), nullable=True),
    sa.Column('url_info_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['url_info_id'], ['urlinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('redirect')
    op.drop_table('urlinfo')
    # ### end Alembic commands ###
