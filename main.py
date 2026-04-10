from fastapi import FastAPI
from database.database import engine
from city.models import Base
from city.routes import city_router

app = FastAPI()

app.include_router(city_router)

Base.metadata.create_all(bind=engine)