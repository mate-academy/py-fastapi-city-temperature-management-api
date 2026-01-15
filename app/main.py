from fastapi import FastAPI
from database import engine, Base
from routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")

app.include_router(cities.router)
app.include_router(temperatures.router)
