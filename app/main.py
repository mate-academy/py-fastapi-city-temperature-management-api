from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import cities_router, temperatures_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB on startup
    await init_db()
    yield


app = FastAPI(
    title="City Temperature Management API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(cities_router)
app.include_router(temperatures_router)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "City Temperature Management API is running."}
