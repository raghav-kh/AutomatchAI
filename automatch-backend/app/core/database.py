from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif settings.database_url.startswith("postgresql"):
    # Supabase's connection pooler (pgbouncer, typically port 6543) runs in
    # transaction mode and doesn't support server-side prepared statements.
    # Disabling them here is harmless against a direct connection (port 5432)
    # too, so it's safe to always set for Postgres.
    connect_args = {"prepare_threshold": None}
else:
    connect_args = {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
