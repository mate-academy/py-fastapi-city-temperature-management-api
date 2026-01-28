from fastapi import FastAPI, APIRouter

from core import settings
from routers import *

app = FastAPI()

api_router = APIRouter(prefix=settings.API_PREFIX)
api_router.include_router(cities_router)
api_router.include_router(temperature_router)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
