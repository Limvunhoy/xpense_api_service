import os
from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

# PG_USER = os.getenv("POSTGRES_USER")
# PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
# PG_PORT = os.getenv("POSTGRES_PORT", "5432")
# PG_DB = os.getenv("POSTGRES_DB")

# DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(
    DATABASE_URL,
    echo=True,         # Set True to log SQL queries
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def create_db_and_tables():
    """Create tables in PostgreSQL (dev use only - prefer Alembic for prod)."""
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# === Local File DB ===
# DATABASE_URL = "sqlite:///xpense.db"
# CONNECT_ARGS = {"check_same_thread": False}

# engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     """Dependency function to provide database session."""
#     with Session(engine) as session:
#         yield session
