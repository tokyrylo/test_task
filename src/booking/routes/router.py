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
    """
    Retrieve a list of all available rooms with a minimum specified capacity.

    This endpoint returns all rooms that are available for booking with a capacity
    greater than or equal to the specified `min_capacity`.

    Args:
        min_capacity: The minimum capacity of the rooms to be returned. Defaults to 0.
        service: The booking service dependency.

    Returns:
        A list of `RoomOut` objects representing the available rooms.
    """

    rooms = await service.get_available_rooms(min_capacity=min_capacity)
    return rooms


@router.get("/rooms", response_model=List[RoomOut])
async def list_available_rooms(min_capacity: int = Query(0, ge=0), service: BookingService = Depends(get_booking_service)):
    """
    Returns a list of all rooms that are available for booking and have a capacity of at least `min_capacity`.

    Args:
        min_capacity: The minimum capacity of the rooms to be returned. Defaults to 0.

    Returns:
        A list of `RoomOut` objects representing the available rooms.
    """
    rooms = await service.get_available_rooms(min_capacity)
    return rooms

@router.get("/rooms/{room_id}/availability")
async def check_room_availability(room_id: int, date_: date, service: BookingService = Depends(get_booking_service)):

    """
    Check the availability of a specific room on a given date.

    Args:
        room_id: The ID of the room to check availability for.
        date_: The date to check the room's availability.
        service: The booking service dependency.

    Returns:
        A dictionary containing the room ID, the date checked, and a boolean
        indicating whether the room is available on that date.
    """

    available = await service.room_repo.is_available(room_id, date_)
    return {"room_id": room_id, "date": date_, "available": available}

@router.post("/bookings", response_model=BookingOut)
async def create_booking(booking_in: BookingCreate, service: BookingService = Depends(get_booking_service)):
    """
    Create a new booking.

    If the booking is successful, a `BookingOut` object is returned.
    If the booking is unsuccessful, a 400 error is returned with a description of the error.
    """
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
    """
    Cancel an existing booking by its ID.

    This endpoint allows a user to cancel a booking if it is more than 2 hours
    before the booking start time. If the cancellation is successful, a confirmation
    message is returned. Otherwise, an error is raised.

    Args:
        booking_id: The ID of the booking to cancel.
        service: The booking service dependency.

    Returns:
        A dictionary containing a confirmation message if the cancellation
        is successful.

    Raises:
        HTTPException: If the booking is not found or if it is too late to cancel.
    """

    current_time = datetime.utcnow()
    try:
        await service.cancel_booking(booking_id, current_time)
        return {"detail": "Booking cancelled"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
