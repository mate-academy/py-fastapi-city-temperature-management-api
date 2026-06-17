from fastapi import FastAPI

from app.city.router import router as city_router
from app.temperature.router import router as temp_router
from settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(city_router, prefix="/cities", tags=["Cities"])
app.include_router(temp_router, prefix="/temperatures", tags=["Temperatures"])


@app.get("/")
def read_root() -> dict:
    return {"message": "Welcome to City Temperature Management API"}
