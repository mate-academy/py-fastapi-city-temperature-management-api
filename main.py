from fastapi import FastAPI
from database import Base, engine
from city.router import router as city_router
from temperature.router import router as temperature_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(city_router)
app.include_router(temperature_router)

