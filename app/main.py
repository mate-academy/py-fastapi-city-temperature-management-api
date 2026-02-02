from fastapi import FastAPI

from app.routers import city_router, temperature_router

app = FastAPI(
    title="Weather API",
    description="API for managing cities and their temperature data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(city_router)
app.include_router(temperature_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
