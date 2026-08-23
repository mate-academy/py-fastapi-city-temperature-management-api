from contextlib import asynccontextmanager

from fastapi import FastAPI

from city import router as city_router
from db import models
from db.database import engine
from temperature import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(city_router.router)
app.include_router(temperature_router.router)
