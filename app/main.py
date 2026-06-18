from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.models import models
from app.database import Base
from app.routers import cities, temperatures


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables on startup if they don't exist yet."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="City Temperature API",
    description=(
        "Manage cities and fetch their current temperatures from Open-Meteo "
        "(free, no API key required)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["health"])
def health_check():
    """Simple liveness probe."""
    return {"status": "ok", "message": "City Temperature API is running."}