"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-10 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("full_name", sa.String(length=128), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "specialists",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("full_name", sa.String(length=128), nullable=False),
        sa.Column("specialty", sa.String(length=32), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_specialists_specialty", "specialists", ["specialty"])

    op.create_table(
        "requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("tenant_name", sa.String(length=128), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("work_type", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("volume_hours", sa.Integer(), nullable=False),
        sa.Column("desired_time", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_requests_work_type", "requests", ["work_type"])

    op.create_table(
        "brigades",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("request_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["request_id"], ["requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "brigade_specialists",
        sa.Column("brigade_id", sa.Integer(), nullable=False),
        sa.Column("specialist_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["brigade_id"], ["brigades.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["specialist_id"], ["specialists.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("brigade_id", "specialist_id"),
    )


def downgrade() -> None:
    op.drop_table("brigade_specialists")
    op.drop_table("brigades")
    op.drop_index("ix_requests_work_type", table_name="requests")
    op.drop_table("requests")
    op.drop_index("ix_specialists_specialty", table_name="specialists")
    op.drop_table("specialists")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
