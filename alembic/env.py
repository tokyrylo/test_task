import asyncio
from logging.config import fileConfig
from alembic import context
from src.database import metadata, get_sync_engine
from src.config import get_settings

config = context.config
fileConfig(config.config_file_name) if config.config_file_name else None

settings = get_settings()
DATABASE_URL = str(settings.DATABASE_URL).replace("postgresql+asyncpg", "postgresql")
config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = get_sync_engine()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
