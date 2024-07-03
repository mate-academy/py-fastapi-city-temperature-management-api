from fastapi import FastAPI

from app.database import init_db
from app.routers import cities, temperatures

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(
    temperatures.router, prefix="/temperatures", tags=["temperatures"]
)

