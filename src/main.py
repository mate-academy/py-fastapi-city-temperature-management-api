from fastapi import FastAPI

from routes.city import router as city_router
from routes.temperature import router as temperature_router


app = FastAPI()

app.include_router(city_router, prefix="/cities", tags=["city"])
app.include_router(
    temperature_router,
    prefix="/temperatures",
    tags=["temperature"]
)
