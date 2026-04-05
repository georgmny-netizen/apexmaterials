from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.models.rfq import RFQStatus

class RFQCreate(BaseModel):
    company_name: str = Field(..., max_length=255)
    contact_name: str = Field(..., max_length=255)
    email: EmailStr
    material: str | None = Field(default=None, max_length=255)
    specification: str
    notes_from_requester: str | None = None

class RFQResponse(BaseModel):
    id: UUID
    inquiry_number: str
    company_name: str
    contact_name: str
    email: EmailStr
    material: str | None
    specification: str
    notes_from_requester: str | None
    status: RFQStatus
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}

class RFQStatusUpdate(BaseModel):
    to_status: RFQStatus
    changed_by: str | None = None
    comment: str | None = None

class RFQHistoryResponse(BaseModel):
    id: UUID
    from_status: str | None
    to_status: str
    changed_by: str | None
    comment: str | None
    changed_at: datetime

    model_config = {"from_attributes": True}

class RFQInternalNoteCreate(BaseModel):
    author: str | None = None
    body: str

class RFQInternalNoteResponse(BaseModel):
    id: UUID
    author: str | None
    body: str
    created_at: datetime

    model_config = {"from_attributes": True}
