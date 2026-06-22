from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import cities
from app.routers import temperatures

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)
