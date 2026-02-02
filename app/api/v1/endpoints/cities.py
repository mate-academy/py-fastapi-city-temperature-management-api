from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import city as city_crud
from app.db.session import get_session
from app.schemas.city import CityCreate, CityRead, CityUpdate
from app.models import City

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city(
    city_in: CityCreate,
    session: AsyncSession = Depends(get_session),
) -> City:
    return await city_crud.create_city(session, city_in)


@router.get("", response_model=list[CityRead])
async def list_cities(session: AsyncSession = Depends(get_session)) -> list[City]:
    return await city_crud.get_cities(session)


@router.get("/{city_id}", response_model=CityRead)
async def get_city(city_id: int, session: AsyncSession = Depends(get_session)) -> City:
    city = await city_crud.get_city(session, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.put("/{city_id}", response_model=CityRead)
async def update_city(
    city_id: int,
    city_in: CityUpdate,
    session: AsyncSession = Depends(get_session),
) -> City:
    city = await city_crud.get_city(session, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return await city_crud.update_city(session, city, city_in)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, session: AsyncSession = Depends(get_session)) -> None:
    city = await city_crud.get_city(session, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    await city_crud.delete_city(session, city)
    return None
