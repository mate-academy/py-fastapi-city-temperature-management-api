from database import engine, Base
from app.models.city import City
from app.models.temperature import Temperature

from fastapi import FastAPI

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)

Base.metadata.create_all(engine)
