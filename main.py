from fastapi import FastAPI

from city.routes import router as city_router
from temperature.routes import router as temperature_router


app = FastAPI(
    title="City temperature management",
    description="Homework project"
)

app.include_router(city_router, tags=["city"])
app.include_router(temperature_router, tags=["temperature"])
