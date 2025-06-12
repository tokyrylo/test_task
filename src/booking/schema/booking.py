from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    people_count: int

class BookingOut(BaseModel):
    id: int
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True
