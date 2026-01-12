from fastapi import FastAPI
from .database import engine, Base
from .routers import cities, temperatures

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Weather Manager",
    description="A CRUD API for cities and automatic temperature fetching.",
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)

@app.get("/")
def root():
    return {"message": "Welcome to the City Weather API. Go to /docs for the UI."}
