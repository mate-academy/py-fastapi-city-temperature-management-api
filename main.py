from fastapi import FastAPI

from city import models as city_models
from temperature import models as temperature_models
from city import router as city_router
from temperature import router as temperature_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)
