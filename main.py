from contextlib import asynccontextmanager

from fastapi import FastAPI

from city.router import router as city_router
from database import engine, Base

from temperature.router import router as temp_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan
)


app.include_router(city_router)
app.include_router(temp_router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello city temperature service user"}
