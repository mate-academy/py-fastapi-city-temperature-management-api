from fastapi import FastAPI

from .database import Base, engine
from .routers import cities, temperatures

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="City & Temperature API")

# Routers (two "apps/components")
app.include_router(cities.router)
app.include_router(temperatures.router)
