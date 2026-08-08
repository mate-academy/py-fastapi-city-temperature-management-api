from fastapi import FastAPI

from city_crud_api.api.router import router as city_router
from temperature_api.router import router as temperature_router

app = FastAPI(
    title="City Temperature Management API",
    description="City CRUD and historical weather data API.",
)

app.include_router(city_router)
app.include_router(temperature_router)
