from fastapi import FastAPI
from .database import engine, Base
from .routers import cities, temperatures

app = FastAPI(title="City Temperature Management API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])


@app.get("/")
def root():
    return {"message": "City Temperature Management API"}
