"""climmobShare - I18nRegsection - table relationship

Revision ID: 9ca963f65ebd
Revises: 3ab4cb6630be
Create Date: 2021-08-10 14:41:29.114775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9ca963f65ebd"
down_revision = "3ab4cb6630be"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "i18n_regsection", type_="primary")
    op.create_primary_key(
        "pk_i18n_regsection",
        "i18n_regsection",
        ["project_id", "section_id", "lang_code"],
    )

    op.create_foreign_key(
        op.f("fk_i18n_regsection_project_id_regsection"),
        "i18n_regsection",
        "regsection",
        ["project_id", "section_id"],
        ["project_id", "section_id"],
    )
    op.create_foreign_key(
        op.f("fk_i18n_regsection_lang_code_i18n"),
        "i18n_regsection",
        "i18n",
        ["lang_code"],
        ["lang_code"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "i18n_regsection", type_="primary")
    op.create_primary_key(
        "pk_i18n_regsection",
        "i18n_regsection",
        ["user_name", "project_cod", "section_id", "lang_code"],
    )

    op.drop_constraint(
        op.f("fk_i18n_regsection_lang_code_i18n"), "i18n_regsection", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_i18n_regsection_project_id_regsection"),
        "i18n_regsection",
        type_="foreignkey",
    )
    # ### end Alembic commands ###