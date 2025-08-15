import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load .env variables into environment
load_dotenv()

# Read required env vars
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
USE_POOLER = os.getenv("SUPABASE_USE_POOLER",
                       "false").strip().lower() == "true"

if not SUPABASE_PASSWORD or not SUPABASE_PROJECT_ID:
    raise EnvironmentError(
        "Missing SUPABASE_PASSWORD or SUPABASE_PROJECT_ID in environment variables.")

# Determine DB host and user based on connection type
if USE_POOLER:
    DB_USER = f"postgres.{SUPABASE_PROJECT_ID}"
    DB_HOST = "aws-1-ap-southeast-1.pooler.supabase.com"
else:
    DB_USER = "postgres"
    DB_HOST = f"db.{SUPABASE_PROJECT_ID}.supabase.co"

# Build connection string
DATABASE_URL = f"postgresql://{DB_USER}:{SUPABASE_PASSWORD}@{DB_HOST}:5432/postgres"

# Create SQLModel engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require",
        "gssencmode": "disable",  # Prevent GSSAPI negotiation issues
    },
)


def create_db_and_tables() -> None:
    """Create all tables defined in SQLModel metadata (dev only)."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Yield a database session."""
    with Session(engine) as session:
        yield session
