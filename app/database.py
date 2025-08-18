# app/database.py
from sqlmodel import SQLModel, create_engine, Session
from app.core.settings import settings


# Select database URL based on ENV
if settings.ENV == "dev":
    DATABASE_URL = (
        f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )

    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

else:
    if not settings.SUPABASE_PROJECT_ID or not settings.SUPABASE_PASSWORD:
        raise EnvironmentError(
            "Missing SUPABASE_PROJECT_ID or SUPABASE_PASSWORD in environment"
        )

    if settings.SUPABASE_USE_POOLER:
        DB_USER = f"postgres.{settings.SUPABASE_PROJECT_ID}"
        DB_HOST = "aws-1-ap-southeast-1.pooler.supabase.com"
    else:
        DB_USER = "postgres"
        DB_HOST = f"db.{settings.SUPABASE_PROJECT_ID}.supabase.co"

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{settings.SUPABASE_PASSWORD}"
        f"@{DB_HOST}:5432/postgres"
    )

    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        connect_args={
            "sslmode": "require",
            "gssencmode": "disable",
        },
    )


def create_db_and_tables() -> None:
    """Create tables only in development."""
    if settings.ENV == "dev":
        SQLModel.metadata.create_all(engine)


def get_session():
    """Yield a database session."""
    with Session(engine) as session:
        yield session
