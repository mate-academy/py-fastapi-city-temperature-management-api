from fastapi import FastAPI
from city.router import router as city_router

app = FastAPI()

app.include_router(city_router, prefix="/api")
