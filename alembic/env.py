"""Alembic environment configuration."""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import SQLModel and models
from sqlmodel import SQLModel
from src.db import NotificationSource, NotificationHistory

# this is the Alembic Config object
config = context.config

# Override sqlalchemy.url from environment if set
if os.getenv("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine

    url = config.get_main_option("sqlalchemy.url")

    # Create engine
    connectable = create_engine(url, poolclass=pool.NullPool)

    # For CockroachDB: patch dialect to handle non-standard version string
    from sqlalchemy.dialects.postgresql import base as pg_base

    original_get_version = pg_base.PGDialect._get_server_version_info

    def patched_get_version_info(self, connection):
        try:
            return original_get_version(self, connection)
        except AssertionError:
            # CockroachDB has non-standard version string
            return (15, 0, 0)

    pg_base.PGDialect._get_server_version_info = patched_get_version_info

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
