from fastapi import FastAPI

from app.city.router import router as city_app
from app.temperature.router import router as temperature_app

app = FastAPI()

app.include_router(city_app)
app.include_router(temperature_app)


@app.get("/")
def index():
    return {"message": "Welcome to the City-Temperature-Management-API"}
