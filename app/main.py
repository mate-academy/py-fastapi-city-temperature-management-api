from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.city.router import router as city_router
from app.config import settings
from app.database import Base, engine

# Import models so they are registered on Base.metadata before create_all.
from app.city import models as city_models  # noqa: F401
from app.temperature import models as temperature_models  # noqa: F401
from app.temperature.router import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {"message": "City Temperature Management API. See /docs."}
