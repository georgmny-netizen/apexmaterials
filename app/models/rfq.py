import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class RFQStatus(str, enum.Enum):
    submitted = "submitted"
    in_review = "in_review"
    clarification_required = "clarification_required"
    quoted = "quoted"
    rejected = "rejected"
    closed = "closed"

class RFQ(Base):
    __tablename__ = "rfqs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inquiry_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255))
    contact_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(320), index=True)
    material: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specification: Mapped[str] = mapped_column(Text)
    notes_from_requester: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RFQStatus] = mapped_column(Enum(RFQStatus, name="rfq_status"), default=RFQStatus.submitted, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    history: Mapped[list["RFQStatusHistory"]] = relationship(back_populates="rfq", cascade="all, delete-orphan")
    internal_notes: Mapped[list["RFQInternalNote"]] = relationship(back_populates="rfq", cascade="all, delete-orphan")

class RFQStatusHistory(Base):
    __tablename__ = "rfq_status_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rfqs.id", ondelete="CASCADE"), index=True)
    from_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    to_status: Mapped[str] = mapped_column(String(64))
    changed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    rfq: Mapped["RFQ"] = relationship(back_populates="history")

class RFQInternalNote(Base):
    __tablename__ = "rfq_internal_notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rfqs.id", ondelete="CASCADE"), index=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    rfq: Mapped["RFQ"] = relationship(back_populates="internal_notes")
