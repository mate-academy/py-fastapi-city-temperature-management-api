from fastapi import FastAPI
from .db import Base, engine
from .routers import cities

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City CRUD API")

app.include_router(cities.router)
