from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud
from city.models import City
from city.schemas import CityRead, CityCreate
from dependencies import get_session

router = APIRouter(prefix="/cities",
                   tags=["cities"])


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city(
        data: CityCreate,
        session: AsyncSession = Depends(get_session)
) -> CityRead:
    return await crud.create_city(session, data)


@router.get("/{city_id}", response_model=CityRead)
async def get_city(city_id: int, session: AsyncSession = Depends(get_session)):
    city = await crud.get_city(session, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, session: AsyncSession = Depends(get_session)):
    city = await crud.get_city(session, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    await crud.delete_city(session, city)


@router.get("", response_model=list[CityRead])
async def get_cities(session: AsyncSession = Depends(get_session)) -> list[City]:
    result = await crud.get_cities(session)
    return result
