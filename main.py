from fastapi import FastAPI

from cities.router import router as cities_router
from temperatures.router import router as temp_router

app = FastAPI()

app.include_router(cities_router, prefix="/cities", tags=["Cities"])
app.include_router(temp_router, prefix="/temperatures", tags=["Temperature"])

@app.get("/")
def root():
    return {"message": "Welcome to the City Temperature Management API!"}