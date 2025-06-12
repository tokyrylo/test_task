from fastapi import FastAPI

from src.booking.routes.router import router as booking_router

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


app.include_router(booking_router)
