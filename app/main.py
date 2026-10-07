from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.city import router as cities_router
from app.api.temperature import router as temperatures_router
from app.db.engine import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="City & Temperature Management API",
    description="API for managing cities and monitoring current temperature",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cities_router)
app.include_router(temperatures_router)
