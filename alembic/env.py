from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from src.config import get_settings
from src.database import metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
async_url = str(settings.DATABASE_URL)
sync_url = async_url.replace("postgresql+asyncpg", "postgresql")  # заміна async на sync

config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = metadata


def run_migrations_offline():
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
