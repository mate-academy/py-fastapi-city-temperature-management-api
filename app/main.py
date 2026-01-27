from fastapi import FastAPI
from app.routers import cities, temperatures


app = FastAPI(
    title="City Temperature API",
    description="API for managing cities and their temperature data",
    version="1.0.0"
)


app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to City Temperature API",
        "version": "1.0.0",
        "endpoints": {
            "cities": "/cities",
            "temperatures": "/temperatures",
            "documentation": "/docs"
        }
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
