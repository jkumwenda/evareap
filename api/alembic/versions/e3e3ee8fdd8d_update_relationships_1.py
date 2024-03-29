"""update relationships 1

Revision ID: e3e3ee8fdd8d
Revises: 2305dc34a44b
Create Date: 2023-11-21 21:27:00.794448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3e3ee8fdd8d'
down_revision: Union[str, None] = '2305dc34a44b'
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
