from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Weather Tracking API", version="1.0.0")
app.include_router(cities.router)
app.include_router(temperatures.router)

@app.get("/")
def root():
    return {"message": "Welcome to the City Weather API", "docs_url": "/docs"}
