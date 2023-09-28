from fastapi import FastAPI

from city_api import router as city_router
from temperature_api import router as temp_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temp_router.router)
