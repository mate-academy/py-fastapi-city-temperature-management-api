from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import engine, Base
from city.router import router as city_router
from temperature.router import router as temp_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan, title="City Temperature API")
app.include_router(city_router)
app.include_router(temp_router)


