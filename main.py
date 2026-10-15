from fastapi import FastAPI

from cities.router import router as cities_router
from settings import settings
from temperatures.router import router as temperatures_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(cities_router)
app.include_router(temperatures_router)
