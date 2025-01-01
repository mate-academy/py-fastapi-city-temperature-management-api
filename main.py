from fastapi import FastAPI

from city_crud_api import router as city_crud_api_router
from temperature_api import router as temperature_api_router

app = FastAPI()

app.include_router(city_crud_api_router.router)
app.include_router(temperature_api_router.router)
