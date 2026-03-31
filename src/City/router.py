from os import environ
from typing import List, AsyncGenerator
from httpx import AsyncClient
from fastapi import APIRouter, HTTPException, status
from src.City import schemas, crud
from src.base_schemas import CityDetail
from src.config import settings
from dependencies import AsyncDB


router = APIRouter()
CITY_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


async def check_city_temperature(name: str) -> float | None:
    async with AsyncClient() as client:
        res = (
            await client.get(
                settings.WEATHER_API_BASE_URL,
                params={
                    "key": environ["WEATHER_API_KEY"],
                    "q": name,
                }
            )
        ).json()
    if "error" not in res:
        return res["current"]["temp_c"]

@router.post("/", response_model=CityDetail, status_code=status.HTTP_201_CREATED)
async def create_city(city: schemas.CityCreateOrUpdate, db: AsyncDB):
    if await check_city_temperature(city.name):
        result = await crud.create_new_city(db=db, city=city)
        return result
    raise CITY_NOT_FOUND


@router.get("/", response_model=List[CityDetail])
async def get_list_cities(db: AsyncDB):
    return await crud.get_all_cities(db=db)


@router.get("/{city_id}", response_model=schemas.CityRead)
async def get_city(city_id: int, db: AsyncDB):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise CITY_NOT_FOUND
    return city


@router.put("/{city_id}", response_model=CityDetail)
async def put_update_city(city_id: int, city: schemas.CityCreateOrUpdate, db: AsyncDB):
    if await check_city_temperature(city.name):
        updated_city = await crud.update_city(db=db, city_id=city_id, city=city)
        if updated_city:
            return updated_city
    raise CITY_NOT_FOUND


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncDB):
    deleted_city = await crud.delete_city_by_id(db=db, city_id=city_id)
    if not deleted_city:
        raise CITY_NOT_FOUND
