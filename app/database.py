from sqlite3 import OperationalError
import time
from sqlmodel import SQLModel, create_engine, Session
from app.core.settings import settings
import logging


def test_connection(retries: int = 5, delay: int = 2):
    """Check DB connection with retry"""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                logging.info(
                    f"Database connected successfully: {result.scalar()}")
                return True
        except OperationalError as e:
            logging.warning(
                f"Database connection failed (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    logging.error("All retries failed. Database not reachable.")
    return False


logging.basicConfig(level=logging.INFO)

# Database URL
if settings.ENV != "dev":
    if not settings.SUPABASE_PROJECT_ID or not settings.SUPABASE_PASSWORD:
        raise RuntimeError("Missing Supabase env vars")

    DB_USER = "postgres"  # not using pooler
    DB_HOST = f"db.{settings.SUPABASE_PROJECT_ID}.supabase.co"  # direct host
    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{settings.SUPABASE_PASSWORD}@{DB_HOST}:5432/postgres"
    )

else:
    DATABASE_URL = (
        f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )

    # if not settings.SUPABASE_PROJECT_ID or not settings.SUPABASE_PASSWORD:
    #     raise RuntimeError("Missing Supabase env vars")

    # DB_USER = f"postgres.{settings.SUPABASE_PROJECT_ID}" if settings.SUPABASE_USE_POOLER else "postgres"
    # DB_HOST = (
    #     "aws-1-ap-southeast-1.pooler.supabase.com"
    #     if settings.SUPABASE_USE_POOLER
    #     else f"db.{settings.SUPABASE_PROJECT_ID}.supabase.co"
    # )

    # DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{settings.SUPABASE_PASSWORD}@{DB_HOST}:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"} if settings.ENV != "dev" else {}
)


def test_connection():
    """Check DB connection without crashing"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logging.info(f"Database connected successfully: {result.scalar()}")
    except Exception as e:
        logging.warning(f"Database connection failed: {e}")


def create_db_and_tables():
    """Create tables, safe for dev only, does not crash in prod"""
    if settings.ENV == "dev":
        try:
            SQLModel.metadata.create_all(engine)
            logging.info("Tables created successfully")
        except Exception as e:
            logging.warning(f"Failed to create tables: {e}")


def get_session():
    """DB session generator"""
    with Session(engine) as session:
        yield session
