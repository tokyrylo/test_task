from pydantic import BaseModel

class RoomOut(BaseModel):
    id: int
    name: str
    capacity: int

    class Config:
        orm_mode = True
