from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cities, temperatures


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="City Temperature API",
    description=(
        "A REST API for managing cities and tracking their current temperatures. "
        "Temperature data is fetched from the free Open-Meteo weather service."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "City Temperature API is running."}
