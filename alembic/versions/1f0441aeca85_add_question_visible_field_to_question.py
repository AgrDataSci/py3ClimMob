"""add question_visible field to question

Revision ID: 1f0441aeca85
Revises: a71511f93b07
Create Date: 2019-10-04 15:35:30.399950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1f0441aeca85"
down_revision = "a71511f93b07"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "question",
        sa.Column(
            "question_visible",
            sa.Integer(),
            server_default=sa.text("'1'"),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("question", "question_visible")
    # ### end Alembic commands ###
