"""climmobShare - AssDetail - table relationship

Revision ID: 379b6800b8a4
Revises: 03ec5a4ca463
Create Date: 2021-08-10 10:38:17.393841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session
from climmob.models.climmobv4 import AssDetail, Project

# revision identifiers, used by Alembic.
revision = "379b6800b8a4"
down_revision = "03ec5a4ca463"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "assdetail", type_="primary")
    op.create_primary_key(
        "pk_assdetail", "assdetail", ["project_id", "ass_cod", "question_id"]
    )

    op.add_column(
        "assdetail",
        sa.Column("section_project_id", sa.String(length=80), nullable=False),
    )

    session = Session(bind=op.get_bind())
    try:
        projects = session.execute("Select * from project")
        for project in projects:
            session.execute(
                "UPDATE assdetail SET section_project_id = '"
                + project.project_id
                + "' WHERE (project_id = '"
                + project.project_id
                + "') "
            )
    except Exception as e:
        print(str(e))
        exit(1)

    session.commit()

    op.create_index(
        "fk_assessment_asssection1_idx",
        "assdetail",
        ["section_project_id", "section_id"],
        unique=False,
    )
    op.create_foreign_key(
        op.f("fk_assdetail_question_id_question"),
        "assdetail",
        "question",
        ["question_id"],
        ["question_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_assdetail_project_id_assessment"),
        "assdetail",
        "assessment",
        ["project_id", "ass_cod"],
        ["project_id", "ass_cod"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_assdetail_section_project_id_asssection"),
        "assdetail",
        "asssection",
        ["section_project_id", "section_assessment", "section_id"],
        ["project_id", "ass_cod", "section_id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "assdetail", type_="primary")
    op.create_primary_key(
        "pk_assdetail",
        "assdetail",
        ["user_name", "project_cod", "ass_cod", "question_id"],
    )

    op.drop_constraint(
        op.f("fk_assdetail_section_project_id_asssection"),
        "assdetail",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_assdetail_project_id_assessment"), "assdetail", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_assdetail_question_id_question"), "assdetail", type_="foreignkey"
    )
    op.drop_index("fk_assessment_asssection1_idx", table_name="assdetail")
    op.drop_column("assdetail", "section_project_id")
    # ### end Alembic commands ###