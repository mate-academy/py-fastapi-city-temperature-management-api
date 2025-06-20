from fastapi import FastAPI

from src.routes.city import router as city_router
from src.routes.temperature import router as temperature_router

app = FastAPI(title="temperature-management", description="Temperature Management API")
app.include_router(city_router, tags=["city"])
app.include_router(temperature_router, tags=["temperature"])
