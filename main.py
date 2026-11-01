from fastapi import FastAPI

from models.city import Base
from city.routers import city_router
from database import engine
from temperature.routers import temp_router

app = FastAPI()

app.include_router(city_router)
app.include_router(temp_router)


@app.get("/")
def home():
    return "Hello!"
