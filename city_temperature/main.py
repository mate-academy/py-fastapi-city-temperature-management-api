from fastapi import FastAPI
from city_temperature.database import Base, engine
from city_temperature.routers import city_router, temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature API",
    description="API for managing cities and tracking temperature history.",
    version="1.0.0",
)

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/", tags=["root"])
def root() -> dict:
    return {"message": "Welcome to the City Temperature API!"}
