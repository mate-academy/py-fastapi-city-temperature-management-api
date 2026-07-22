from fastapi import FastAPI

from app.routers.city import router as city_router
from app.routers.temperature import router as temperature_router


app = FastAPI()
app.include_router(city_router)
app.include_router(temperature_router)
