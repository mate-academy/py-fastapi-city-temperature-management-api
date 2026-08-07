from fastapi import APIRouter, FastAPI

from routers.city import city
from routers.temperature import temperature

app = FastAPI()

internal_router = APIRouter()
internal_router.include_router(city)
app.include_router(internal_router)
app.include_router(temperature)
