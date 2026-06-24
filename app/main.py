from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import Base, engine
from app.cities.router import router as cities_router
from app.temperatures.router import router as temps_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="City Weather Management API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(cities_router)
app.include_router(temps_router)


@app.get("/")
async def root():
    return {"message": "Welcome to City Weather API. Go to /docs for Swagger documentation."}
