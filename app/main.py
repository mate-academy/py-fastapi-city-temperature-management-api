from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing cities and their temperature data",
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
async def root():
    return {
        "message": "City Temperature Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

