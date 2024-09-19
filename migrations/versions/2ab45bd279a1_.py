"""empty message

Revision ID: 2ab45bd279a1
Revises: a5cffa318ac2
Create Date: 2024-09-19 11:36:39.977129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ab45bd279a1'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(length=20), nullable=True))
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('last_name')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
