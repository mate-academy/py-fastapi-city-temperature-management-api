from fastapi import FastAPI
from .database import engine, Base
from .routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WeatherAPI City Tracker",
    description="Manage cities and fetch their current temperatures using WeatherAPI.",
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def root():
    return {"message": "API is running. Visit /docs for Swagger UI."}
