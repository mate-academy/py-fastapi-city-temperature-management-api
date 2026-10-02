from fastapi import FastAPI

from weather_app.app.config import get_settings
from weather_app.app.database import Base, engine
from weather_app.app.routers import cities, temperatures

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "app": settings.app_name, "docs": "/docs"}
