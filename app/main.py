from fastapi import FastAPI

from app.routers import city_router, temperature_router
from app.db.database import init_db


init_db()
app = FastAPI()


app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the City Temperature Management API!"}