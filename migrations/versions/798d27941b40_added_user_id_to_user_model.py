"""Added user_id to User model

Revision ID: 798d27941b40
Revises: 
Create Date: 2023-09-01 22:29:40.706441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '798d27941b40'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=50), nullable=True))
        batch_op.create_unique_constraint(None, ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###