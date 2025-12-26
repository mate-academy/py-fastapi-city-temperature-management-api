from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.models import Base
from database.sqlite import engine
from routers.cities import cities_router
from routers.temperatures import temps_router


@asynccontextmanager
async def create_base():
    async with engine.connect() as eng:
        await eng.run_sync(Base.metadata.create_all)


app = FastAPI(
    title="Temperatures for Cities",
    lifespan=create_base
)

app.include_router(cities_router)
app.include_router(temps_router)
