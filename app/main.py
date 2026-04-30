from fastapi import FastAPI

from app.database import Base, engine
import app.models
from app.routers import city, temperature

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)
