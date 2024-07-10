from fastapi import FastAPI
from routers import city, temperature
from db.engine import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city.router, prefix="/cities", tags=["cities"])
app.include_router(
    temperature.router, prefix="/temperatures", tags=["temperatures"]
)
