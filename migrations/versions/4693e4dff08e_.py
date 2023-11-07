"""empty message

Revision ID: 4693e4dff08e
Revises: 06b46f299438
Create Date: 2023-11-07 03:46:26.107779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4693e4dff08e'
down_revision = '06b46f299438'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
