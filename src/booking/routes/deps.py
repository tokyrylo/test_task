from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.booking.schema.room import RoomOut
from src.booking.services.booking_service import BookingService
from src.booking.repository.room_imp import RoomRepository
from src.booking.repository.booking_imp import BookingRepository

async def get_booking_service(session: AsyncSession = Depends(get_async_session)) -> BookingService:
    room_repo = RoomRepository(session)
    booking_repo = BookingRepository(session)
    return BookingService(room_repo, booking_repo)