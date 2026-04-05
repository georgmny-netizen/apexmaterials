from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Replace postgresql:// with postgresql+psycopg:// for psycopg3 driver
database_url = settings.database_url.replace("postgresql://", "postgresql+psycopg://")
engine = create_engine(database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
