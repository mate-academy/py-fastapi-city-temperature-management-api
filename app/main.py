from fastapi import FastAPI
from .routers import city, temperature


app = FastAPI()


@app.get("/")
def read_root():
    return{"message": "Welcome to the City-Temperature API"}


app.include_router(city.router)
app.include_router(temperature.router)
