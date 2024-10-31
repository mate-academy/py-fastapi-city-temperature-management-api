import os

from dotenv import load_dotenv
from fastapi import FastAPI

from cities.routers import router as city_routers

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

WEATHER_API_URL = os.getenv("WEATHER_API_URL")

app = FastAPI()


app.include_router(city_routers)
