from fastapi import FastAPI

from database import SessionLocal
from routers.cities import router as cities_router
from routers.temperatures import router as temperatures_router

app = FastAPI()

app.include_router(cities_router)
app.include_router(temperatures_router)

app = FastAPI()

async def get_db():
    async with SessionLocal() as session:
        yield session
