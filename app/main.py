from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routers import cities, temperatures


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI application to manage city data and record live temperature histories.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["Health Check"])
def root():
    return {"status": "healthy", "project": settings.PROJECT_NAME}
