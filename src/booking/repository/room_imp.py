from typing import List, Optional, Dict, Any
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.booking.repository.room import IRoomRepository
from src.booking.schema.room import Room
from src.database import rooms, bookings 

class RoomRepository(IRoomRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Room]:
        query = select(rooms).where(rooms.c.id == id)
        result = await self.session.execute(query)
        row = result.first()
        if row:
            return Room(**row._mapping)
        return None

    async def list(self, filters: Dict[str, Any] = None) -> List[Room]:
        query = select(rooms)
        if filters:
            for key, val in filters.items():
                query = query.where(getattr(rooms.c, key) == val)
        result = await self.session.execute(query)
        return [Room(**row._mapping) for row in result.fetchall()]

    async def list_available(self, min_capacity: int = 0) -> List[Room]:
        query = select(rooms).where(rooms.c.capacity >= min_capacity)
        result = await self.session.execute(query)
        return [Room(**row._mapping) for row in result.fetchall()]

    async def is_available(self, room_id: int, date_: date) -> bool:
        query = select(bookings).where(
            bookings.c.room_id == room_id,
            bookings.c.start_time <= date_,
            bookings.c.end_time >= date_,
        )
        result = await self.session.execute(query)
        return result.first() is None

    async def add(self, entity: Room) -> Room:
        pass

    async def update(self, entity: Room) -> None:
        pass

    async def delete(self, id: int) -> None:
        pass
