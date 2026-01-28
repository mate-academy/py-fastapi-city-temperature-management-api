from fastapi import FastAPI
from api_v1.cities.router import router as cities_router
from api_v1.temperatures.router import router as temperatures_router

app = FastAPI()

app.include_router(cities_router)
app.include_router(temperatures_router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
