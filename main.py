from fastapi import FastAPI

from app.city import city_api
from app.temperature import temperature_api
app = FastAPI()

app.include_router(city_api.router, prefix="/api", tags=["cities"])
app.include_router(temperature_api.router, prefix="/api", tags=["temperatures"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the city temperature management API!"}
