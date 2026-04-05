"""create rfq tables

Revision ID: 0001_create_rfq_tables
Revises: 
Create Date: 2026-04-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_create_rfq_tables"
down_revision = None
branch_labels = None
depends_on = None

rfq_status = sa.Enum(
    "submitted",
    "in_review",
    "clarification_required",
    "quoted",
    "rejected",
    "closed",
    name="rfq_status",
)

def upgrade() -> None:
    rfq_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "rfqs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("inquiry_number", sa.String(length=32), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("contact_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("material", sa.String(length=255), nullable=True),
        sa.Column("specification", sa.Text(), nullable=False),
        sa.Column("notes_from_requester", sa.Text(), nullable=True),
        sa.Column("status", rfq_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_rfqs_inquiry_number", "rfqs", ["inquiry_number"], unique=True)
    op.create_index("ix_rfqs_email", "rfqs", ["email"], unique=False)
    op.create_index("ix_rfqs_status", "rfqs", ["status"], unique=False)

    op.create_table(
        "rfq_status_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("rfq_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("from_status", sa.String(length=64), nullable=True),
        sa.Column("to_status", sa.String(length=64), nullable=False),
        sa.Column("changed_by", sa.String(length=255), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_rfq_status_history_rfq_id", "rfq_status_history", ["rfq_id"], unique=False)

    op.create_table(
        "rfq_internal_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("rfq_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_rfq_internal_notes_rfq_id", "rfq_internal_notes", ["rfq_id"], unique=False)

def downgrade() -> None:
    op.drop_index("ix_rfq_internal_notes_rfq_id", table_name="rfq_internal_notes")
    op.drop_table("rfq_internal_notes")
    op.drop_index("ix_rfq_status_history_rfq_id", table_name="rfq_status_history")
    op.drop_table("rfq_status_history")
    op.drop_index("ix_rfqs_status", table_name="rfqs")
    op.drop_index("ix_rfqs_email", table_name="rfqs")
    op.drop_index("ix_rfqs_inquiry_number", table_name="rfqs")
    op.drop_table("rfqs")
    rfq_status.drop(op.get_bind(), checkfirst=True)
