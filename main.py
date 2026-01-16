from fastapi import FastAPI
from city import router as city_router
from temperature import router as temperature_router
from city.models import City
from database import engine, Base
from temperature.models import Temperature
app = FastAPI()


@app.on_event("startup")
async def startup():
    # 3. Create all tables from your models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # 4. Tables now exist in database
    print("Database tables created!")

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
