from typing import List

from fastapi import APIRouter, HTTPException

from crud import (
    check_city_by_name_in_db,
    create_city,
    get_all_cities,
    get_city_by_id,
    update_city,
    remove_city
)
from db.database import SessionDep
from schemas import (
    CityListSchema,
    CityCreateSchema,
    CityRetrieveSchema,
    CityUpdateSchema,
    MessageSchema
)

router = APIRouter()


@router.post("/cities/", response_model=CityListSchema)
async def add_city(city: CityCreateSchema, db: SessionDep):
    if await check_city_by_name_in_db(db=db, city_name=city.name):
        raise HTTPException(status_code=400, detail="City already exists")
    return await create_city(db, city)


@router.get("/cities/", response_model=List[CityListSchema])
async def list_cities(db: SessionDep):

    cities = await get_all_cities(db=db)
    if not cities:
        raise HTTPException(status_code=404, detail="Cities not found")
    return cities


@router.get("/cities/{city_id}", response_model=CityRetrieveSchema)
async def retrieve_city(city_id: int, db: SessionDep):
    city = await get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=CityListSchema)
async def edit_city(city_id: int, city_update: CityUpdateSchema, db: SessionDep):
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await update_city(db=db, db_city=db_city, city_update=city_update)


@router.delete("/cities/{city_id}", response_model=MessageSchema)
async def delete_city(city_id: int, db: SessionDep):
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    await remove_city(db, db_city)
    return MessageSchema(message=f"City {db_city.name} was successfully removed!")
