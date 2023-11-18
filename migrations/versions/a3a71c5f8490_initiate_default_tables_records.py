"""initiate_default_tables_records

Revision ID: a3a71c5f8490
Revises: 3700130a79d3
Create Date: 2023-11-18 05:22:57.739476

"""

from app.models.default_category import insert_default_categories


# revision identifiers, used by Alembic.
revision = 'a3a71c5f8490'
down_revision = '3700130a79d3'
branch_labels = None
depends_on = None


def upgrade():
    insert_default_categories()


def downgrade():
    pass
