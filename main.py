from fastapi import FastAPI

from cities.models import City  # noqa: F401
from cities.router import router as cities_router
from temperatures.models import Temperature  # noqa: F401
from temperatures.router import router as temperatures_router

app = FastAPI()

app.include_router(cities_router)
app.include_router(temperatures_router)
