from dotenv import load_dotenv
from fastapi import FastAPI

import city.models
import temperature.models
from city.router import router as city_router
from database import engine
from temperature.router import router as temperature_router

load_dotenv()

city.models.Base.metadata.create_all(bind=engine)
temperature.models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")

app.include_router(city_router)
app.include_router(temperature_router)
