from typing import List, Protocol

from datetime import date

from src.booking.repository.base import IRepository
from src.booking.schema.room import RoomOut


class IRoomRepository(IRepository[RoomOut, int], Protocol):
    async def list_available(self, min_capacity: int = 0) -> List[RoomOut]:
        ...

    async def is_available(self, room_id: int, date: date) -> bool:
        ...
