from fastapi import FastAPI
from app.database import Base, engine
from app.routes import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Manager",
    description="CRUD API для міст + API для збору й перегляду історії температур",
    version="1.0.0",
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["root"])
def root():
    return {"message": "City Temperature Manager API is running"}