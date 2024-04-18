from fastapi import FastAPI

from db import database
import models
from temperature import temp_routers
from city import city_routers

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(city_routers.router)
app.include_router(temp_routers.router)
