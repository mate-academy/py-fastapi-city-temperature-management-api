from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cities, temperatures


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="City Temperature Management API",
    description="CRUD for cities and temperature history with Open-Meteo updates",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
