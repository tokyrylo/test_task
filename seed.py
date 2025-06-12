import asyncio
from datetime import datetime, timedelta

from sqlalchemy import insert
from src.database import async_session, rooms, bookings

async def seed_data():
    async with async_session() as session:
        async with session.begin():

            await session.execute(bookings.delete())
            await session.execute(rooms.delete())

            room_data = [
                {"id": 1, "name": "Room A", "capacity": 5},
                {"id": 2, "name": "Room B", "capacity": 10},
                {"id": 3, "name": "Room C", "capacity": 3},
            ]
            await session.execute(insert(rooms), room_data)

            now = datetime.utcnow()
            booking_data = [
                {
                    "room_id": 1,
                    "user_id": 101,
                    "start_time": now + timedelta(hours=1),
                    "end_time": now + timedelta(hours=2),
                },
                {
                    "room_id": 2,
                    "user_id": 102,
                    "start_time": now + timedelta(days=1),
                    "end_time": now + timedelta(days=1, hours=2),
                },
            ]
            await session.execute(insert(bookings), booking_data)

        print("✅ Seed completed")

if __name__ == "__main__":
    asyncio.run(seed_data())
