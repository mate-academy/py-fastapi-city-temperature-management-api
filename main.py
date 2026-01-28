from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base
from db.session import get_db, engine
from schemas.city import CityReadSchema, CityCreateSchema
from schemas.temperature import TemperatureReadSchema, TemperatureCreateSchema
from crud.city import (
    get_all_cities,
    create_city,
    get_city_by_id,
    delete_city,
    update_city,
)
from crud.temperature import (
    create_temperature,
    get_all_temperatures,
    delete_temperature,
    get_temperatures_by_city_id,
    update_temperature
)
from crud.exceptions import CityAlreadyExistsException


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/temperatures/", response_model=TemperatureReadSchema)
async def create_temp(
    temp_in: TemperatureCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await create_temperature(db, temp_in)


@app.get("/temperatures/", response_model=list[TemperatureReadSchema])
async def read_temps(
    db: AsyncSession = Depends(get_db),
    city_id: int | None = None
):
    if city_id is not None:
        return await get_temperatures_by_city_id(db, city_id)
    return await get_all_temperatures(db)


@app.put("/temperatures/{temp_id}", response_model=TemperatureReadSchema)
async def update_temp_endpoint(
    temp_id: int,
    temp_update: TemperatureCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_temperature(db, temp_id, temp_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Temperature record not found")
    return updated


@app.delete("/temperatures/{temp_id}")
async def delete_temp(temp_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_temperature(db, temp_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Temperature record not found")
    return {"message": "Temperature record deleted"}



@app.post("/cities/", response_model=CityReadSchema)
async def create_city_endpoint(
    city_in: CityCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_city(db, city_in)
    except CityAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/cities/", response_model=list[CityReadSchema])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await get_all_cities(db)


@app.get("/cities/{city_id}", response_model=CityReadSchema)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=CityReadSchema)
async def update_city_endpoint(
    city_id: int,
    city_update: CityCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_city(db, city_id, city_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@app.delete("/cities/{city_id}")
async def delete_city_endpoint(city_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted"}
