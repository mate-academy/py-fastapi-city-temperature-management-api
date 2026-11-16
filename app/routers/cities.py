"""CRUD endpoints for tracked cities."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import City
from app.schemas import CityCreate, CityRead, CityUpdate


router = APIRouter(prefix="/cities", tags=["cities"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city(city_data: CityCreate, session: SessionDep) -> City:
    city = City(**city_data.model_dump())
    session.add(city)
    await session.commit()
    await session.refresh(city)
    return city


@router.get("", response_model=list[CityRead])
async def list_cities(session: SessionDep) -> list[City]:
    result = await session.scalars(select(City).order_by(City.id))
    return list(result.all())


@router.get("/{city_id}", response_model=CityRead)
async def get_city(city_id: int, session: SessionDep) -> City:
    city = await session.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityRead)
async def update_city(city_id: int, city_data: CityUpdate, session: SessionDep) -> City:
    city = await session.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    for field, value in city_data.model_dump(exclude_unset=True).items():
        setattr(city, field, value)

    await session.commit()
    await session.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, session: SessionDep) -> Response:
    city = await session.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    await session.delete(city)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

