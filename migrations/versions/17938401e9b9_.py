"""empty message

Revision ID: 17938401e9b9
Revises: 6258ad9ece19
Create Date: 2025-02-12 17:37:52.141967

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17938401e9b9'
down_revision = '6258ad9ece19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payout', schema=None) as batch_op:
        batch_op.alter_column('payment_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('seller_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('transaction_id',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payout', schema=None) as batch_op:
        batch_op.alter_column('transaction_id',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('seller_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('payment_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
