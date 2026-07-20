from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from db.database import Base, engine
from cities.router import router as cities_router
from temperature.router import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(cities_router)
app.include_router(temperature_router)


if __name__ == "__main__":
    uvicorn.run("main:app")
