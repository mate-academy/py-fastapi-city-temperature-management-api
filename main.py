from fastapi import FastAPI

from city.router import router as city_router
from db import database
from temperature.router import router as temperature_router

app = FastAPI()

database.Base.metadata.create_all(database.engine)

app.include_router(city_router)
app.include_router(temperature_router)
