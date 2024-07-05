from fastapi import FastAPI
from app.routers import cities, temperatures
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(
    temperatures.router, prefix="/temperatures", tags=["temperatures"]
)
