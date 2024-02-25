"""update relationships 4

Revision ID: af4f059a9969
Revises: e3e3ee8fdd8d
Create Date: 2023-11-21 21:43:32.269859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af4f059a9969'
down_revision: Union[str, None] = 'e3e3ee8fdd8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'departments', 'users', ['head'], ['id'])
    op.create_foreign_key(None, 'users', 'departments', ['department'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'departments', type_='foreignkey')
    # ### end Alembic commands ###