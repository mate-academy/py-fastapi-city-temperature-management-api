from fastapi import FastAPI

from database import engine, Base
from city_crud_api.routers import router as city_routers
from temperature_api.routers import router as temperature_routers


app = FastAPI()

app.include_router(city_routers, prefix="/api/v1", tags=["cities"])
app.include_router(temperature_routers, prefix="/api/v1", tags=["temperatures"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
