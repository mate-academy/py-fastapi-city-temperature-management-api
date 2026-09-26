from contextlib import asynccontextmanager

from fastapi import FastAPI
from city import router as city_router
from database import create_db_and_tables
from temperature import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(city_router.router)
app.include_router(temperature_router.router)