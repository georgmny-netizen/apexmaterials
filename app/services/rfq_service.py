from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.rfq import RFQ, RFQStatus, RFQStatusHistory, RFQInternalNote
from app.schemas.rfq import RFQCreate, RFQStatusUpdate, RFQInternalNoteCreate

def _generate_inquiry_number(db: Session) -> str:
    count = db.scalar(select(func.count()).select_from(RFQ)) or 0
    next_number = count + 1
    return f"RFQ-{next_number:06d}"

def create_rfq(db: Session, payload: RFQCreate) -> RFQ:
    rfq = RFQ(
        inquiry_number=_generate_inquiry_number(db),
        company_name=payload.company_name,
        contact_name=payload.contact_name,
        email=str(payload.email),
        material=payload.material,
        specification=payload.specification,
        notes_from_requester=payload.notes_from_requester,
        status=RFQStatus.submitted,
    )
    db.add(rfq)
    db.flush()

    db.add(
        RFQStatusHistory(
            rfq_id=rfq.id,
            from_status=None,
            to_status=RFQStatus.submitted.value,
            changed_by="system",
            comment="RFQ created",
        )
    )
    db.commit()
    db.refresh(rfq)
    return rfq

def list_rfqs(db: Session, status: RFQStatus | None = None) -> list[RFQ]:
    stmt = select(RFQ).order_by(RFQ.created_at.desc())
    if status is not None:
        stmt = stmt.where(RFQ.status == status)
    return list(db.scalars(stmt).all())

def get_rfq_or_404(db: Session, rfq_id: UUID) -> RFQ:
    rfq = db.get(RFQ, rfq_id)
    if not rfq:
        raise ValueError("RFQ not found")
    return rfq

def update_status(db: Session, rfq: RFQ, payload: RFQStatusUpdate) -> RFQ:
    previous = rfq.status.value if rfq.status else None
    rfq.status = payload.to_status
    db.add(
        RFQStatusHistory(
            rfq_id=rfq.id,
            from_status=previous,
            to_status=payload.to_status.value,
            changed_by=payload.changed_by,
            comment=payload.comment,
        )
    )
    db.commit()
    db.refresh(rfq)
    return rfq

def add_internal_note(db: Session, rfq: RFQ, payload: RFQInternalNoteCreate) -> RFQInternalNote:
    note = RFQInternalNote(rfq_id=rfq.id, author=payload.author, body=payload.body)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_history(db: Session, rfq_id: UUID) -> list[RFQStatusHistory]:
    stmt = select(RFQStatusHistory).where(RFQStatusHistory.rfq_id == rfq_id).order_by(RFQStatusHistory.changed_at.asc())
    return list(db.scalars(stmt).all())
