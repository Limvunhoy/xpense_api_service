from app.core.settings import settings
from app.database import DATABASE_URL, engine
from app.models import *  # all your SQLModel models
import sys
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

# Add app folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import settings, engine, and models AFTER sys.path

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Dynamically set the DB URL
db_url = str(DATABASE_URL)

# Ensure SSL mode for Supabase
if settings.ENV != "dev" and "sslmode" not in db_url:
    if "?" in db_url:
        db_url += "&sslmode=require"
    else:
        db_url += "?sslmode=require"

config.set_main_option("sqlalchemy.url", db_url)

# Metadata for auto-migration detection
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Run migrations in offline mode (no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in online mode (connect to DB)."""
    # Use the app's engine directly
    connectable = engine

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Choose offline or online based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
