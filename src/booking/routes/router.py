from typing import List
from datetime import datetime, date

from fastapi import APIRouter, Depends, Query, HTTPException

from src.booking.routes.deps import get_booking_service
from src.booking.schema.booking import BookingOut, BookingCreate
from src.booking.schema.room import RoomOut
from src.booking.services.booking_service import BookingService


router = APIRouter()

@router.get("/", response_model=List[RoomOut])
async def list_rooms(
    min_capacity: int = Query(0, ge=0),
    service: BookingService = Depends(get_booking_service)
):
    rooms = await service.get_available_rooms(min_capacity=min_capacity)
    return rooms


@router.get("/rooms", response_model=List[RoomOut])
async def list_available_rooms(min_capacity: int = Query(0, ge=0), service: BookingService = Depends(get_booking_service)):
    rooms = await service.get_available_rooms(min_capacity)
    return rooms

@router.get("/rooms/{room_id}/availability")
async def check_room_availability(room_id: int, date_: date, service: BookingService = Depends(get_booking_service)):
    available = await service.room_repo.is_available(room_id, date_)
    return {"room_id": room_id, "date": date_, "available": available}

@router.post("/bookings", response_model=BookingOut)
async def create_booking(booking_in: BookingCreate, service: BookingService = Depends(get_booking_service)):
    try:
        booking = await service.book_room(
            room_id=booking_in.room_id,
            user_id=booking_in.user_id,
            start_time=booking_in.start_time,
            end_time=booking_in.end_time,
            people_count=booking_in.people_count
        )
        return booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/bookings/{booking_id}")
async def cancel_booking(booking_id: int, service: BookingService = Depends(get_booking_service)):
    current_time = datetime.utcnow()
    try:
        await service.cancel_booking(booking_id, current_time)
        return {"detail": "Booking cancelled"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
