import logging

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cities, temperatures

# Set up basic logging for the application
logging.basicConfig(level=logging.INFO)

# Create database tables on startup (SQLite-friendly)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API", version="0.1.0")

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def healthcheck():
    return {"status": "ok", "service": "city-temperature-api"}

