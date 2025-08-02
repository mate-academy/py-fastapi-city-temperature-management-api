from fastapi import FastAPI, Depends
from database import engine, get_db
import models
from routers import cities, temperatures

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature API",
    description="API for managing cities and temperature data",
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)

@app.get("/")
def root():
    return {"message": "City Temperature Management API"}
