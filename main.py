from fastapi import FastAPI
from city_crud_api.router import router as city_router
from temperature_api.router import router as temperature_router
from database import engine
from city_crud_api.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city_router, prefix="/cities", tags=["cities"])
app.include_router(
    temperature_router, prefix="/temperatures", tags=["temperatures"]
)
