from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey

metadata = MetaData()

rooms = Table(
    "rooms", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("capacity", Integer, nullable=False),
)

bookings = Table(
    "bookings", metadata,
    Column("id", Integer, primary_key=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("start_time", DateTime, nullable=False),
    Column("end_time", DateTime, nullable=False),
)
