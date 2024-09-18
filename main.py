from fastapi import FastAPI

from city.router import router as city_router
from temperature.router import router as temperature_router

app = FastAPI()

app.include_router(city_router, prefix="/cities")
app.include_router(temperature_router, prefix="/temperatures")


@app.get("/")
def root_test():
    return {"message": "test page"}
