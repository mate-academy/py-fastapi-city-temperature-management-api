from fastapi import FastAPI

from app.city import routers as city_router
from temperature import routers as temperature_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)
