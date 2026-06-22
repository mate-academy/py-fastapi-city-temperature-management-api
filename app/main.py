from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import cities

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(cities.router)
