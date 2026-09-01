from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import cities, temperatures


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="City Temperature API",
    description=(
        "API for managing cities "
        "and storing their temperature history."
    ),
)


app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def root():
    return {
        "message": "City Temperature API is running"
    }
