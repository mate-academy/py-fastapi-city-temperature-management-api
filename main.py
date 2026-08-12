from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from city import router as cities_router
from temperature import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(cities_router.router)
app.include_router(temperature_router.router)
