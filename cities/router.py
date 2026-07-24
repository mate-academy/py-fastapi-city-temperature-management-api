from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import create_city, delete_city_by_id, get_all_cities, get_city_by_id
from cities.schemas import SCity, SCityCreate
from database import get_async_session

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/")
async def add_city(
    city_data: SCityCreate,
    session: AsyncSession = Depends(get_async_session),
) -> SCity:
    city = await create_city(session, data=city_data)
    return SCity.model_validate(city)


@router.get("/")
async def get_cities(session: AsyncSession = Depends(get_async_session)) -> List[SCity]:
    cities = await get_all_cities(session=session)
    return [SCity.model_validate(city) for city in cities]


@router.get("/{city_id}/")
async def get_city(
    city_id: int, session: AsyncSession = Depends(get_async_session)
) -> SCity:
    city = await get_city_by_id(session=session, id_=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return SCity.model_validate(city)


@router.delete("/{city_id}/", status_code=204)
async def delete_city(
    city_id: int, session: AsyncSession = Depends(get_async_session)
) -> None:
    is_deleted = await delete_city_by_id(session=session, id_=city_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="City not found")
