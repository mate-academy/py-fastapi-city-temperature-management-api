import models
from fastapi import FastAPI
from database import engine
from routers import cities, temperatures


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="City Temperature Management API")

app.include_router(cities.router)
app.include_router(temperatures.router)

@app.get("/")
def root() -> dict:
    return {"message": "Welcome to City Temperature Management API"}
