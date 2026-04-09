from fastapi import FastAPI

from dependencies import lifespan
from city import city_router
from temperature import temperature_router

app = FastAPI(lifespan=lifespan)
app.include_router(city_router.router)
app.include_router(temperature_router.router)
