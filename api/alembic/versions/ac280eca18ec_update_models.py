"""update models

Revision ID: ac280eca18ec
Revises: 
Create Date: 2023-11-21 21:15:04.492390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ac280eca18ec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'departments', 'users', ['head'], ['id'])
    op.alter_column('manufacturers', 'email',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.create_index(op.f('ix_manufacturers_email'), 'manufacturers', ['email'], unique=True)
    op.create_index(op.f('ix_manufacturers_id'), 'manufacturers', ['id'], unique=False)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_foreign_key(None, 'users', 'departments', ['department'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.alter_column('users', 'email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
    op.drop_index(op.f('ix_manufacturers_id'), table_name='manufacturers')
    op.drop_index(op.f('ix_manufacturers_email'), table_name='manufacturers')
    op.alter_column('manufacturers', 'email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
    op.drop_constraint(None, 'departments', type_='foreignkey')
    # ### end Alembic commands ###
