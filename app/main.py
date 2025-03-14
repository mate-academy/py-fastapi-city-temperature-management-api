from fastapi import FastAPI
from ..routers import city, temperature
from ..database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)