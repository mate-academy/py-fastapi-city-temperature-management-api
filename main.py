from contextlib import asynccontextmanager

from fastapi import FastAPI

from city import models as city_models  # noqa: F401
from city.router import router as city_router
from database import Base, engine
from temperature import models as temperature_models  # noqa: F401
from temperature.router import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="City & Temperature Management API", lifespan=lifespan)

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
async def root():
    return {"message": "City & Temperature Management API"}
