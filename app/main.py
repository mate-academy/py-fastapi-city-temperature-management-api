# app/main.py
from fastapi import FastAPI
from app.api.city_routes import router as city_router
from app.api.temperature_routes import router as temperature_router
from app.database import engine
from app.models import Base

app = FastAPI()
app.include_router(city_router)
app.include_router(temperature_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to City Temperature API"}
