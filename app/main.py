from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from routers.cities import router as cities_router
from routers.temperatures import router as temperatures_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(cities_router)
app.include_router(temperatures_router)