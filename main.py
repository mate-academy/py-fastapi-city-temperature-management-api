from fastapi import FastAPI
from database import engine, Base
from routers import (city, temperature)


# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Weather API",
    description="API for managing cities and their current temperatures",
    version="1.0.0"
)

app.include_router(city.router)
app.include_router(temperature.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the City Weather API. Visit /docs for documentation."}
