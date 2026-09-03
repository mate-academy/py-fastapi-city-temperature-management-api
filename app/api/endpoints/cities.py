from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import City
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
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> City:
    result = await db.execute(
        select(City).where(City.id == city_id)
    )
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return city


@router.put(
    "/{city_id}",
    response_model=CityRead,
)
async def update_city(
    city_id: int,
    city_data: CityCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> City:
    result = await db.execute(
        select(City).where(City.id == city_id)
    )
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

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
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(City).where(City.id == city_id)
    )
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    await db.delete(city)
    await db.commit()
