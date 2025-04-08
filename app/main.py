from fastapi import FastAPI
from app.database import engine, Base
from app.routers import city as city_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(city_router.router)
