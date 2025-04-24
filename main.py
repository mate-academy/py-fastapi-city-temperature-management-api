from fastapi import FastAPI
from database import Base, engine
from city.routers import router as city_router
from temperature.routers import router as temperature_router
import asyncio

app = FastAPI()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(city_router)
app.include_router(temperature_router)