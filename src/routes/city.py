from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.sqlite_session import get_db
from schemes.city import (
    CreateCityRequestSchema,
    CreateCityResponseSchema, ListCitiesResponseSchema, CityDetailResponseSchema, CityChangeRequestSchema
)
from database.models import CityModel

BASE_URL = "/cities/"

router = APIRouter()

DB = Annotated[AsyncSession, Depends(get_db)]

@router.post(
    "/",
    response_model=CreateCityResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(
        data: CreateCityRequestSchema,
        db: DB,
):
    city_stmt = select(CityModel).where(CityModel.name == data.name)
    city_result = await db.execute(city_stmt)
    city = city_result.scalar_one_or_none()
    if city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The city with name {data.name} already exists."
        )

    city = CityModel(
        name=data.name,
        additional_info=data.additional_info,
    )

    db.add(city)
    await db.commit()
    await db.refresh(city)
    return CreateCityResponseSchema.model_validate(city, from_attributes=True)


@router.get(
    "/",
    response_model=ListCitiesResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_cities(
        db: DB,
        page: Annotated[int, Query(ge=1)] = 1,
        per_page: Annotated[int, Query(ge=1, le=5)] = 2,
):
    offset = (page - 1) * per_page

    total_cities_stmt = select(func.count(CityModel.id))
    total_cities_result = await db.execute(total_cities_stmt)
    total_cities = total_cities_result.scalar() or 0

    if total_cities == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities."
        )

    total_pages = (total_cities + per_page - 1) // per_page

    cities_stmt = select(CityModel).offset(offset).limit(per_page)
    cities_result = await db.execute(cities_stmt)
    cities = cities_result.scalars().all()

    prev_page = f"{BASE_URL}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{BASE_URL}?page{page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "cities": cities,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_cities": total_cities
    }


@router.get(
    "/{city_id}/",
    response_model=CityDetailResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_single_city(
        city_id: int,
        db: DB,
):
    city_stmt = select(CityModel).where(CityModel.id == city_id)
    city_result = await db.execute(city_stmt)
    city = city_result.scalar_one_or_none()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found.",
        )

    return CityDetailResponseSchema.model_validate(city, from_attributes=True)


@router.put(
    "/{city_id}/",
    response_model=CityDetailResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def change_city_info(
        city_id: int,
        data: CityChangeRequestSchema,
        db: DB
):
    city_stmt = select(CityModel).where(CityModel.id == city_id)
    city_result = await db.execute(city_stmt)
    city = city_result.scalar_one_or_none()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found.",
        )

    if data.name:
        city.name = data.name
    if data.additional_info:
        city.additional_info = data.additional_info

    await db.commit()
    await db.refresh(city)
    return CityDetailResponseSchema.model_validate(city, from_attributes=True)


@router.delete(
    "/{city_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_city(
        city_id: int,
        db: DB,
):
    city_stmt = select(CityModel).where(CityModel.id == city_id)
    city_result = await db.execute(city_stmt)
    city = city_result.scalar_one_or_none()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found.",
        )

    await db.delete(city)
    await db.commit()
    return {
        "message": f"City {city.name} was successfully deleted."
    }
