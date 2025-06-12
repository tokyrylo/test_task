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
from sqlalchemy.orm import Session
from sqlalchemy.orm import registry
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM

mapper_registry = registry()
engine_sync = create_engine(DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

sync_session = sessionmaker(engine_sync, class_=Session, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with sync_session() as session:
        try:
            yield session
        finally:
            await session.close()


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
