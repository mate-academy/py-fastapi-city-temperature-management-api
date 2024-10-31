from fastapi import FastAPI
from cities.routers import router as city_router
from temperatures.routers import router as temperature_router

app = FastAPI()

# Include the city router
app.include_router(city_router, tags=["cities"])
app.include_router(temperature_router, tags=["temperature"])
