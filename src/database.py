from sqlalchemy import MetaData, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import get_settings

settings = get_settings()

# Async setup
DATABASE_ASYNC_URL = str(settings.DATABASE_URL)
async_engine = create_async_engine(settings.DATABASE_ASYNC_URL)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Sync setup for migrations
DATABASE_SYNC_URL = DATABASE_ASYNC_URL.replace("postgresql+asyncpg", "postgresql")
sync_engine = None  # Will be created when needed for migrations
sync_session = None

metadata = MetaData()

# Tables
rooms = Table(
    "rooms",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("capacity", Integer, nullable=False),
)

bookings = Table(
    "bookings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("start_time", DateTime, nullable=False),
    Column("end_time", DateTime, nullable=False),
)


async def get_async_session():
    async with async_session() as session:
        yield session


def get_sync_engine():
    global sync_engine
    if sync_engine is None:
        from sqlalchemy import create_engine

        sync_engine = create_engine(DATABASE_SYNC_URL)
    return sync_engine


def get_db_sync():
    global sync_session
    if sync_session is None:
        from sqlalchemy.orm import Session, sessionmaker

        sync_session = sessionmaker(
            get_sync_engine(), class_=Session, expire_on_commit=False
        )
    session = sync_session()
    try:
        yield session
    finally:
        session.close()
