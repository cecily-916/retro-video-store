"""empty message

Revision ID: dc1f37a402dc
Revises: 2c6ae8584941
Create Date: 2021-11-14 20:39:32.156200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc1f37a402dc'
down_revision = '2c6ae8584941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('rental_customer_id_fkey', 'rental', type_='foreignkey')
    op.drop_constraint('rental_video_id_fkey', 'rental', type_='foreignkey')
    op.create_foreign_key(None, 'rental', 'video', ['video_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'rental', 'customer', ['customer_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rental', type_='foreignkey')
    op.drop_constraint(None, 'rental', type_='foreignkey')
    op.create_foreign_key('rental_video_id_fkey', 'rental', 'video', ['video_id'], ['id'])
    op.create_foreign_key('rental_customer_id_fkey', 'rental', 'customer', ['customer_id'], ['id'])
    # ### end Alembic commands ###