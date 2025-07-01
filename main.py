from contextlib import asynccontextmanager

from fastapi import FastAPI

from city_api.routers import router
from city_api.database import engine
from city_api.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "HIII"}

app.include_router(router)

