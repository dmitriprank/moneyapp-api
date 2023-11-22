"""empty message

Revision ID: 9be7a950c10a
Revises: a3a71c5f8490
Create Date: 2023-11-22 02:48:49.319660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9be7a950c10a'
down_revision = 'a3a71c5f8490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=512), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
