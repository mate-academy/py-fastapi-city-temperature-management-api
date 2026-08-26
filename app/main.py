from fastapi import FastAPI
from .database import engine, Base
from .routers import cities, temperatures


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing cities and fetching their temperatures",
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)

@app.get("/")
def root():
    return {"message": "Welcome to the City Temperature Management API! Go to /docs for the Swagger UI."}