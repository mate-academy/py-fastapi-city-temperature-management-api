from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import cities, temperatures

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing cities and temperature history",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "City Temperature Management API"}


app.include_router(cities.router)
app.include_router(temperatures.router)
