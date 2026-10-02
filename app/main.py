from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routers import cities, temperatures


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="City & Temperature Management API",
    version="1.0.0",
    description="API для управління містами та відстеження історії температур.",
    lifespan=lifespan,
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "City & Temperature API працює!"}
