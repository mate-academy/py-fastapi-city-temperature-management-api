from fastapi import FastAPI
from app.database import engine, Base
from app.cities.router import router as cities_router
from app.temperatures.router import router as temperatures_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Weather Management API",
    description="API for tracking cities and their temperature history using automated async fetching.",
    version="1.0.0"
)

app.include_router(cities_router)
app.include_router(temperatures_router)

@app.get("/")
def root():
    return {"message": "Welcome to City Weather API. Go to /docs for interactive Swagger documentation."}
