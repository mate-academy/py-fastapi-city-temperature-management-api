from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def root():
    return {"message": "City Temperature API"}
