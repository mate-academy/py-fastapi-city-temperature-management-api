from fastapi import FastAPI

from app.database import Base, engine
from app.api.cities import router as cities_router
from app.api.temperatures import router as temperatures_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")

app.include_router(cities_router)
app.include_router(temperatures_router)


@app.get("/health")
def health():
    return {"status": "ok"}
