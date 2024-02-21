from fastapi import FastAPI

from city_temperature.routers import router

app = FastAPI()

app.include_router(router)
