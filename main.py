from fastapi import FastAPI

from database import engine
from city_app import models as city_models, router as city_router
from temperature_app import (
    models as temperature_models,
    router as temperature_router,
)


city_models.Base.metadata.create_all(bind=engine)
temperature_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)
