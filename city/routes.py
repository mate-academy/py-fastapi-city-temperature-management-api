from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import (
    create_city,
    get_cities,
    get_cities_by_city_id,
    change_city,
    remove_city
)
from city.schemas import (
    CreateCitySchemas,
    CityBaseSchemas,
    UpdateCitySchemas,
    MessageSchema
)
from dependencies import get_db


router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=CityBaseSchemas)
async def cities(
        city_info: CreateCitySchemas,
        db: AsyncSession = Depends(get_db)
):
    new_city = await create_city(city_data=city_info, db=db)

    return new_city


@router.get("/", response_model=list[CityBaseSchemas])
async def list_cities(db: AsyncSession = Depends(get_db)):
    db_cities = await get_cities(db=db)
    return db_cities


@router.get("/{city_id}", response_model=CityBaseSchemas)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_cities_by_city_id(city_id=city_id, db=db)

    return city


@router.put("/{city_id}", response_model=CityBaseSchemas)
async def update_city(
        city_id: int,
        city_data: UpdateCitySchemas,
        db: AsyncSession = Depends(get_db)
):
    updated_city = await change_city(
        city_id=city_id,
        city_data=city_data,
        db=db
    )

    return updated_city


@router.delete("/cities/{city_id}", response_model=MessageSchema)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await remove_city(city_id=city_id, db=db)

    return result
