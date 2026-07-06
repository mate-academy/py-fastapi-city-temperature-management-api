from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Weather Tracker API",
    description="Junior-level project to track city temperatures dynamically",
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)

@app.get("/")
def root():
    return {"message": "Welcome to City Weather Tracker. Go to /docs for Swagger UI"}
