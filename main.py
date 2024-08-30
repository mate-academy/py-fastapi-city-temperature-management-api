from fastapi import FastAPI

from city_temperature_app.api import city, temperature
from database import Base, engine


app = FastAPI()

app.include_router(city.router, prefix="/api", tags=["cities"])
app.include_router(temperature.router, prefix="/api", tags=["temperatures"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the city temperature management API!"}
