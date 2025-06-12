from typing import List, Protocol

from datetime import datetime, date

from src.booking.repository.base import IRepository
from src.booking.schema.booking import BookingOut


class IBookingRepository(IRepository[BookingOut, int], Protocol):
    async def list_bookings_for_room_on_date(
        self, room_id: int, date: date
    ) -> List[BookingOut]:
        ...

    async def is_conflicting(self, room_id: int, start_time: datetime, end_time: datetime) -> bool:
        ...
