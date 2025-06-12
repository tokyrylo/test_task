from typing import List, Optional, Dict, Any
from datetime import datetime, date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.booking.repository.booking import IBookingRepository
from src.booking.schema.booking import Booking
from src.database import bookings

class BookingRepository(IBookingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Booking]:
        query = select(bookings).where(bookings.c.id == id)
        result = await self.session.execute(query)
        row = result.first()
        if row:
            return Booking(**row._mapping)
        return None

    async def list(self, filters: Dict[str, Any] = None) -> List[Booking]:
        query = select(bookings)
        if filters:
            for key, val in filters.items():
                query = query.where(getattr(bookings.c, key) == val)
        result = await self.session.execute(query)
        return [Booking(**row._mapping) for row in result.fetchall()]

    async def list_bookings_for_room_on_date(self, room_id: int, date_: date) -> List[Booking]:
        query = select(bookings).where(
            bookings.c.room_id == room_id,
            bookings.c.start_time >= datetime.combine(date_, datetime.min.time()),
            bookings.c.end_time <= datetime.combine(date_, datetime.max.time()),
        )
        result = await self.session.execute(query)
        return [Booking(**row._mapping) for row in result.fetchall()]

    async def is_conflicting(self, room_id: int, start_time: datetime, end_time: datetime) -> bool:
        query = select(bookings).where(
            bookings.c.room_id == room_id,
            or_(
                and_(
                    bookings.c.start_time < end_time,
                    bookings.c.end_time > start_time,
                )
            )
        )
        result = await self.session.execute(query)
        return result.first() is not None

    async def add(self, entity: Booking) -> Booking:
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def update(self, entity: Booking) -> None:
        pass

    async def delete(self, id: int) -> None:
        pass
