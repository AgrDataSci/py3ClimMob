"""Create table project_metadata

Revision ID: 56897fe827da
Revises: 9a521581ab46
Create Date: 2023-11-07 10:12:51.476800

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "56897fe827da"
down_revision = "9a521581ab46"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "project_metadata",
        sa.Column("project_id", sa.Unicode(length=64), nullable=False),
        sa.Column("md_coordinator", sa.Unicode(length=100), nullable=False),
        sa.Column(
            "md_crops", mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"), nullable=True
        ),
        sa.Column("md_year", sa.Integer(), nullable=True),
        sa.Column("md_tricot_project", sa.Unicode(length=120), nullable=True),
        sa.Column(
            "md_objective",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_collaborators",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_experimental_design",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_steps_followed",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_special_features",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_how_varieties_were_selected",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_how_participants_were_selected",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_geographic_areas",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_selection_criteria_used",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_how_participants_approached_recruitment",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_where_recruidment_place",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_how_recruitment_formalised",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_participants_compensated",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_participants_approached_participate", sa.Integer(), nullable=True
        ),
        sa.Column(
            "md_how_tricot_explained",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_training_sessions",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_follow_up_procedures",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_how_was_data_collected",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_how_were_results_devolved",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_instructions_given",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_additional_inputs_provided",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.Column(
            "md_varieties",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.project_id"],
            name=op.f("fk_project_metadata_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "project_id", "md_coordinator", name=op.f("pk_project_metadata")
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("project_metadata")
    # ### end Alembic commands ###