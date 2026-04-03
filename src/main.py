from fastapi import FastAPI
from src.City.router import router as city_router
from src.City.models import City
from src.Temperature.router import router as temperature_router
from src.Temperature.models import Temperature
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.include_router(router=city_router, prefix="/cities")
app.include_router(router=temperature_router, prefix="/temperatures")
