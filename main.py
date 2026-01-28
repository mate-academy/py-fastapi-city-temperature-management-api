from fastapi import FastAPI

from db import engine, Base
from routers import cities, temperatures

app = FastAPI(title="City Temperature API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(cities.router)
app.include_router(temperatures.router)
