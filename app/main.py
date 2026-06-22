from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Management API",
    description="Manage cities and track their historical temperature data.",
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
