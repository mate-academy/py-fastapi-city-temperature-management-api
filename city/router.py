from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from dependencies import get_data_base, Paginator
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities_list(
    pagination: Paginator,
    data_base: AsyncSession = Depends(get_data_base)
) -> list:
    return await crud.get_all_cities(data_base, **pagination)


@router.post("/cities/")
async def create_city(city: schemas.CityCreate, data_base: AsyncSession = Depends(get_data_base)):
    if await crud.check_city_by_name(data_base=data_base, name=city.name):
        raise HTTPException(status_code=309, detail=f"{city.name} already exists")

    return await crud.create_city(data_base=data_base, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(city_id: int, data: dict, data_base: AsyncSession = Depends(get_data_base)):
    new_city = await crud.update_city(data_base=data_base, city_id=city_id, data=data)
    return new_city


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, data_base: AsyncSession = Depends(get_data_base)):
    city = await crud.get_city_by_id(data_base=data_base, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")
    return city


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, data_base: AsyncSession = Depends(get_data_base)):
    city = await crud.get_city_by_id(data_base=data_base, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    await crud.delete_city(data_base=data_base, city_id=city_id)
    return city
