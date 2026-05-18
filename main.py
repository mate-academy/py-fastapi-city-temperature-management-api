from fastapi import FastAPI
from database import Base, engine
from cities.router import router as cities_router
from temperatures.router import router as temperatures_router

app = FastAPI()

app.include_router(cities_router)
app.include_router(temperatures_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
