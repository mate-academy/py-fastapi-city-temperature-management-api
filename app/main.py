from fastapi import FastAPI

from app.routers.city import city_router
from app.routers.temperature import temperature_router
from app.dependencies import Base, engine

app = FastAPI()
app.include_router(city_router)
app.include_router(temperature_router)

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the City & Temperature API"}
