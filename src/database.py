from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import get_settings

settings = get_settings()

DATABASE_ASYNC_URL = str(settings.DATABASE_URL)

print(settings.DATABASE_URL)

async_engine = create_async_engine(DATABASE_ASYNC_URL)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

DATABASE_SYNC_URL = DATABASE_ASYNC_URL.replace("postgresql+asyncpg", "postgresql")
sync_engine = create_engine(DATABASE_SYNC_URL)
sync_session = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)


async def get_async_session():
    async with async_session() as session:
        yield session


def get_db_sync():
    session = sync_session()
    try:
        yield session
    finally:
        session.close()


metadata = MetaData()
# Таблицы
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
