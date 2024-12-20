from fastapi import FastAPI
from sqlalchemy.orm import Session

from City_CRUD_API import router as city_router
from Temperature_API import router as temperature_router
from database import SessionLocal

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
