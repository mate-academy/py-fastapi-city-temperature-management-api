from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import City
from app.dependencies.cities import get_city_by_id
from app.dependencies.database import get_db
from app.schemas.city import CityCreateUpdate, CityRead


router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post(
    "",
    response_model=CityRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(
    city_data: CityCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> City:
    city = City(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


@router.get(
    "",
    response_model=list[CityRead],
)
async def get_cities(
    db: AsyncSession = Depends(get_db),
) -> list[City]:
    result = await db.execute(select(City))

    return result.scalars().all()


@router.get(
    "/{city_id}",
    response_model=CityRead,
)
async def get_city(
    city: City = Depends(get_city_by_id),
) -> City:
    return city


@router.put(
    "/{city_id}",
    response_model=CityRead,
)
async def update_city(
    city_data: CityCreateUpdate,
    city: City = Depends(get_city_by_id),
    db: AsyncSession = Depends(get_db),
) -> City:

    city.name = city_data.name
    city.additional_info = city_data.additional_info

    await db.commit()
    await db.refresh(city)

    return city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_city(
    city: City = Depends(get_city_by_id),
    db: AsyncSession = Depends(get_db),
) -> None:
    await db.delete(city)
    await db.commit()
