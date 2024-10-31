from fastapi import FastAPI
from src.city.routers import router as cities_router
from src.temperature.routers import router as temperature_router
from src.error_handlers import handle_city_not_found, handle_key_not_configured
from src.exceptions import CityNotFoundError, KeyNotConfigure

app = FastAPI()


app.add_exception_handler(CityNotFoundError, handle_city_not_found)
app.add_exception_handler(KeyNotConfigure, handle_key_not_configured)

app.include_router(cities_router)
app.include_router(temperature_router)
