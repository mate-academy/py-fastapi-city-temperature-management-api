from fastapi import FastAPI

from src.routers import cities
from src.routers import temperatures

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)
