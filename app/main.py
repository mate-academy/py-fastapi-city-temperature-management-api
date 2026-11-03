from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Management API",
    description="A FastAPI application for managing cities and their temperature data",
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to City Temperature Management API",
        "docs": "/docs",
        "endpoints": {
            "cities": "/cities",
            "temperatures": "/temperatures"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
