from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from cities.routers import router as cities_router
from temperature.routers import router as temps_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="City & Temperature App", lifespan=lifespan)

app.include_router(cities_router)
app.include_router(temps_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
