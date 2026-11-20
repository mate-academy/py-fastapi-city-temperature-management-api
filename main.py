from fastapi import FastAPI

from cities.models import City  # noqa: F401
from cities.router import router as cities_router
from temperatures.models import Temperature  # noqa: F401

app = FastAPI()

app.include_router(cities_router)
