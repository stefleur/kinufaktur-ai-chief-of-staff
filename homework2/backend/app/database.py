import os
from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Default to a local SQLite file for development. In production (Render)
# a proper Postgres `DATABASE_URL` environment variable should be set.
DEFAULT_DATABASE_URL = "sqlite:///./kinuflow.db"
# Prefer a standard `DATABASE_URL` (as provided by many PaaS providers);
# fall back to the project-specific `KINUFLOW_DATABASE_URL` and then to
# the local SQLite default.
DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("KINUFLOW_DATABASE_URL", DEFAULT_DATABASE_URL))


class Base(DeclarativeBase):
    pass


def create_database_engine(database_url: str) -> Engine:
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    return create_engine(database_url, connect_args=connect_args)


engine = create_database_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def create_tables() -> None:
    from . import models  # noqa: F401
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        # In some environments a previous partial DDL operation can leave
        # behind catalog entries that cause `create_all` to raise an
        # IntegrityError (e.g. duplicate type names). For robustness in
        # simple deployments we catch and log the error rather than crash
        # the whole application. For real production systems use a proper
        # migration system (Alembic) and careful initialization.
        import logging
        logging.exception("create_tables: non-fatal error while creating tables; continuing")
