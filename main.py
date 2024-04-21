from fastapi import FastAPI

from city import city_router, city_models
from temperature import temp_router, temp_models
from database import engine

city_models.Base.metadata.create_all(bind=engine)
temp_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temp_router.router)
