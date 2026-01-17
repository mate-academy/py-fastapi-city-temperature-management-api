import crud, schemas, models, services
from fastapi import Depends, FastAPI, HTTPException
from database import engine, AsyncSessionLocal
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
app = FastAPI(lifespan=lifespan)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/cities/", response_model=schemas.CityOut, status_code=201)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db, city)

@app.get("/cities/", response_model=list[schemas.City])
async def get_cities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db, skip=skip, limit=limit)

@app.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)

@app.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(city_id: int | None = None ,skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(db=db, city_id=city_id, skip=skip, limit=limit)

@app.post("/temperatures/update", status_code=201)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_cities(db=db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database")
    updated_records = await services.update_weather_for_all_cities(
        db, cities, crud.create_temperature_record
    )

    return updated_records
