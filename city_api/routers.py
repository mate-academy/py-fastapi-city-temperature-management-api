from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.crud import create_city, get_city
from city_api.models import City
from city_api.schemas import CityCreateSchema, CityResponseCreateSchema, CityBaseSchema, CityMessageResponse
from dependencies import get_db

router = APIRouter()


async def checking_existing_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    request = await db.execute(select(City).where(City.id == city_id))
    city = request.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail=f"City with the given ID: {city_id} was not found!")

    return city


@router.post("/cities", response_model=CityResponseCreateSchema)
async def city_create(data: CityCreateSchema, db: AsyncSession = Depends(get_db)):
    return await create_city(data=data, db=db)


@router.get("/cities", response_model=List[CityResponseCreateSchema])
async def get_list_cities(db: AsyncSession = Depends(get_db)):
    return await get_city(db=db)


@router.get("/cities/{city_id}", response_model=CityResponseCreateSchema)
async def get_city_by_id(commons: Annotated[dict, Depends(checking_existing_city_by_id)]):
    return commons


@router.put("/cities/{city_id}", response_model=CityResponseCreateSchema)
async def update_city(
        commons: Annotated[dict, Depends(checking_existing_city_by_id)],
        data_to_update: CityBaseSchema,
        db: AsyncSession = Depends(get_db)
):
    city = commons

    city.name = data_to_update.name
    city.additional_info = data_to_update.additional_info

    await db.commit()
    await db.refresh(city)

    return city


@router.delete("/cities/{city_id}", response_model=CityMessageResponse)
async def delete_city(
        commons: Annotated[dict, Depends(checking_existing_city_by_id)],
        db: AsyncSession = Depends(get_db)
):
    city = commons

    await db.delete(city)
    await db.commit()

    return CityMessageResponse(message="City deleted successfully")
