from fastapi import FastAPI
from app.routers import cities, temperatures

app = FastAPI(
    title="Weather API",
    description="City temperatures tracker",
    version="0.1.0",
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
