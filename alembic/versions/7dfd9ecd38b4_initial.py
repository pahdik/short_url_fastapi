"""initial

Revision ID: 7dfd9ecd38b4
Revises: 
Create Date: 2024-01-15 02:32:50.676678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dfd9ecd38b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('original_urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_url', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('original_url')
    )
    op.create_table('shortened_urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_url_id', sa.Integer(), nullable=False),
    sa.Column('shortened_url', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['original_url_id'], ['original_urls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shortened_urls')
    op.drop_table('original_urls')
    # ### end Alembic commands ###
