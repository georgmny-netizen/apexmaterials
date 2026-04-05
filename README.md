# ApexMaterials Production Backend Foundation

FastAPI + PostgreSQL + SQLAlchemy + Alembic foundation for RFQ workflow.

## Included
- PostgreSQL-ready configuration
- SQLAlchemy 2.0 models
- RFQ status model
- RFQ status history / audit trail
- Internal notes
- Stable API endpoints
- Alembic migration scaffold
- Docker Compose for local PostgreSQL

## RFQ lifecycle
- submitted
- in_review
- clarification_required
- quoted
- rejected
- closed

## Quick start

### 1) Create environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2) Start PostgreSQL
```bash
docker compose up -d db
```

### 3) Run migrations
```bash
alembic upgrade head
```

### 4) Start API
```bash
uvicorn app.main:app --reload
```

## Key endpoints
- `POST /api/v1/rfqs`
- `GET /api/v1/rfqs`
- `GET /api/v1/rfqs/{rfq_id}`
- `POST /api/v1/rfqs/{rfq_id}/status`
- `POST /api/v1/rfqs/{rfq_id}/notes`
- `GET /api/v1/rfqs/{rfq_id}/history`

## Notes
- This foundation keeps auth/roles out of the critical path so the RFQ workflow can stabilize first.
- Auth can be layered later via JWT / session middleware and reviewer/admin roles.
