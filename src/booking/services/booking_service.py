from datetime import datetime, timedelta
from typing import List

from src.booking.repository.room import IRoomRepository
from src.booking.repository.booking import IBookingRepository
from src.booking.schema.booking import BookingOut
from src.booking.schema.room import RoomOut


class BookingService:
    def __init__(self, room_repo: IRoomRepository, booking_repo: IBookingRepository):
        self.room_repo = room_repo
        self.booking_repo = booking_repo

    async def get_available_rooms(self, min_capacity: int = 0) -> List[RoomOut]:
        return await self.room_repo.list_available(min_capacity)

    async def book_room(
        self,
        room_id: int,
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        people_count: int,
    ) -> BookingOut:
        if start_time.minute != 0 or start_time.second != 0:
            raise ValueError("start_time должен быть на целый час")
        if end_time.minute != 0 or end_time.second != 0:
            raise ValueError("end_time должен быть на целый час")
        if (end_time - start_time) > timedelta(hours=4):
            raise ValueError("Максимальная длительность брони — 4 часа")
        if start_time >= end_time:
            raise ValueError("start_time должен быть меньше end_time")

        room = await self.room_repo.get(room_id)
        if not room:
            raise ValueError("Комната не найдена")
        if people_count > room.capacity:
            raise ValueError("Количество людей превышает вместимость комнаты")

        conflict = await self.booking_repo.is_conflicting(room_id, start_time, end_time)
        if conflict:
            raise ValueError("Комната уже занята в этот интервал")

        booking = BookingOut(
            id=0,
            room_id=room_id,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
        )
        return await self.booking_repo.add(booking)

    async def cancel_booking(self, booking_id: int, current_time: datetime) -> None:
        booking = await self.booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Бронь не найдена")
        if booking.start_time - current_time < timedelta(hours=2):
            raise ValueError("Отмена возможна только за 2 часа до начала")
        await self.booking_repo.delete(booking_id)
