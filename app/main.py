from fastapi import FastAPI

from app.cities.router import router as cities_router
from app.temperature.router import router as temperatures_router


app = FastAPI()

@app.get("/")
def root() -> dict:
    return {
        "message": "City Temperature API",
    }

app.include_router(cities_router, prefix="/cities", tags=["cities"])
app.include_router(temperatures_router, prefix="/temperatures", tags=["temperatures"])
