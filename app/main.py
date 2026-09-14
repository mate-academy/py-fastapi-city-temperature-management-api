from fastapi import FastAPI

from app.routers import router
from app import models

app = FastAPI(
    title="City Temperature API",
    description="API for managing cities and temperature history",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "City Temperature API"}
