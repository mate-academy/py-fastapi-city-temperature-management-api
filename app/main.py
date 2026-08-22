gi"""
Application entrypoint.

Wires together the two "apps" described in the requirements as two routers
mounted on a single FastAPI instance:
  - /cities        -> City CRUD
  - /temperatures  -> Temperature fetch + history
"""
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cities, temperatures

# Create tables on startup if they don't already exist. For a real
# production app you'd use Alembic migrations instead; a one-shot
# create_all is fine for this exercise.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Weather API",
    description=(
        "A CRUD API for managing cities plus an API for fetching and "
        "storing current temperature data for those cities."
    ),
    version="1.0.0",
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["health"])
def root():
    """Simple health-check / welcome endpoint."""
    return {"message": "City Weather API is running. See /docs for the API reference."}
