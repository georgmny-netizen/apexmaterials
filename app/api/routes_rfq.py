from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rfq import RFQStatus
from app.schemas.rfq import (
    RFQCreate,
    RFQResponse,
    RFQStatusUpdate,
    RFQHistoryResponse,
    RFQInternalNoteCreate,
    RFQInternalNoteResponse,
)
from app.services.rfq_service import (
    create_rfq,
    list_rfqs,
    get_rfq_or_404,
    update_status,
    add_internal_note,
    get_history,
)

router = APIRouter(prefix="/rfqs", tags=["RFQs"])

@router.post("", response_model=RFQResponse, status_code=201)
def create_rfq_route(payload: RFQCreate, db: Session = Depends(get_db)):
    return create_rfq(db, payload)

@router.get("", response_model=list[RFQResponse])
def list_rfqs_route(
    status: RFQStatus | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_rfqs(db, status=status)

@router.get("/{rfq_id}", response_model=RFQResponse)
def get_rfq_route(rfq_id: UUID, db: Session = Depends(get_db)):
    try:
        return get_rfq_or_404(db, rfq_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.post("/{rfq_id}/status", response_model=RFQResponse)
def update_rfq_status_route(rfq_id: UUID, payload: RFQStatusUpdate, db: Session = Depends(get_db)):
    try:
        rfq = get_rfq_or_404(db, rfq_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return update_status(db, rfq, payload)

@router.get("/{rfq_id}/history", response_model=list[RFQHistoryResponse])
def get_rfq_history_route(rfq_id: UUID, db: Session = Depends(get_db)):
    return get_history(db, rfq_id)

@router.post("/{rfq_id}/notes", response_model=RFQInternalNoteResponse, status_code=201)
def add_internal_note_route(rfq_id: UUID, payload: RFQInternalNoteCreate, db: Session = Depends(get_db)):
    try:
        rfq = get_rfq_or_404(db, rfq_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return add_internal_note(db, rfq, payload)
