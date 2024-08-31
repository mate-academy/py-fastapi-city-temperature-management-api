from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import (
    create_city,
    get_all_cities,
    upgrade_city,
    delete_city_from_db,
    get_city_by_id
)
import city.schemas
from dependencies import get_db

city_router = APIRouter()


@city_router.get("/cities/", response_model=list[city.schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db)

    if cities is None:
        return []

    return cities


@city_router.post("/cities/", response_model=city.schemas.City)
async def create_new_city(
        city: city.schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await create_city(db=db, city_data=city)


@city_router.get("/cities/{city_id}/", response_model=city.schemas.City)
async def get_city(city: city.schemas.City = Depends(get_city_by_id)):
    return city


@city_router.put("/cities/{city_id}/", response_model=city.schemas.City)
async def update_city(
        city_to_update: city.schemas.CityUpdate,
        city: city.schemas.City = Depends(get_city_by_id),
        db: AsyncSession = Depends(get_db)
):
    return await upgrade_city(
        db=db,
        city=city,
        city_to_update=city_to_update
    )


@city_router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(
        city: city.schemas.City = Depends(get_city_by_id),
        db: AsyncSession = Depends(get_db)
):
    await delete_city_from_db(db=db, city=city)
