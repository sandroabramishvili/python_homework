from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:madagascar@postgres-db:5432/hwk66"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency: opens a DB session per request and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
