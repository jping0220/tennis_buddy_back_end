"""changed Class User to TennisUser

Revision ID: 62cc1a1b361a
Revises: d9b31a76b3fa
Create Date: 2023-07-13 09:38:15.966136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62cc1a1b361a'
down_revision = 'd9b31a76b3fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tennis_user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('tennis_level', sa.Float(), nullable=True),
    sa.Column('preferences', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tennis_level', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('zip_code', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('preferences', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('user_id', name='user_pkey')
    )
    op.drop_table('tennis_user')
    # ### end Alembic commands ###
