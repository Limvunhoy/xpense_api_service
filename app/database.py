import time
import logging
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
from app.core.settings import settings
from sqlalchemy.exc import OperationalError

logging.basicConfig(level=logging.INFO)

# -------------------------
# Database URL
# -------------------------
if settings.ENV != "dev":
    if not settings.SUPABASE_PROJECT_ID or not settings.SUPABASE_PASSWORD:
        raise RuntimeError("Missing Supabase env vars")

    DB_USER = "postgres"
    DB_HOST = f"db.{settings.SUPABASE_PROJECT_ID}.supabase.co"
    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{settings.SUPABASE_PASSWORD}"
        f"@{DB_HOST}:5432/postgres?sslmode=require"
    )
else:
    DATABASE_URL = (
        f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )

print("Base Url: ", DATABASE_URL)

# -------------------------
# Engine
# -------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"} if settings.ENV != "dev" else {}
)

# -------------------------
# DB Connection Test
# -------------------------


def test_connection(retries: int = 5, delay: int = 2) -> bool:
    """Test DB connection with retry, safe for Cloud Run."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                logging.info(
                    f"Database connected successfully: {result.scalar()}")
                return True
        except OperationalError as e:
            logging.warning(
                f"Database connection failed (attempt {attempt}/{retries}): {e}"
            )
            time.sleep(delay)
        except Exception as e:
            logging.warning(f"Unexpected DB error: {e}")
            time.sleep(delay)
    logging.error("All retries failed. Database not reachable.")
    return False

# -------------------------
# Create tables (dev only)
# -------------------------


def create_db_and_tables():
    """Create tables safely (only in dev)."""
    if settings.ENV == "dev":
        try:
            SQLModel.metadata.create_all(engine)
            logging.info("Tables created successfully")
        except Exception as e:
            logging.warning(f"Failed to create tables: {e}")

# -------------------------
# Session generator
# -------------------------


def get_session():
    """DB session generator"""
    with Session(engine) as session:
        yield session
