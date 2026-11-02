from fastapi import FastAPI

from cities.routers import router as cities_router
from temperatures.routers import router as temperatures_router

app = FastAPI()
app.include_router(cities_router)
app.include_router(temperatures_router)
