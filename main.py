from fastapi import FastAPI

from routers.city import city_router
from routers.temperature import temperature_router

app = FastAPI()

app.include_router(router=city_router)
app.include_router(router=temperature_router)
