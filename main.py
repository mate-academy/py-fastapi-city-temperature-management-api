from fastapi import FastAPI

from app.city import router as city_router
from app.temperature import router as temperature_router


app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)
