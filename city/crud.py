from typing import Sequence

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models, schemas


async def get_city_by_name_or_none(name: str, db: AsyncSession) -> models.City | None:
    city = await db.execute(select(models.City).filter(models.City.name == name))  # type: ignore
    return city.scalars().first()


async def get_city_by_id_or_404(city_id: int, db: AsyncSession) -> models.City:
    result = await db.execute(select(models.City).filter(models.City.id == city_id))  # type: ignore
    city = result.scalars().first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city  # type: ignore


async def create_city_or_exist(
    city: schemas.CityCreate, db: AsyncSession
) -> models.City:
    existing_city = await get_city_by_name_or_none(city.name, db)
    if existing_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    new_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def get_all_city(db: AsyncSession) -> Sequence[models.City]:
    result = await db.execute(select(models.City))  # type: ignore
    return result.scalars().all()


async def update_city(
    city_id: int, city_data: schemas.CityUpdate, db: AsyncSession
) -> None:
    city = await get_city_by_id_or_404(city_id, db)
    for var, value in vars(city_data).items():
        setattr(city, var, value) if value is not None else None
    await db.commit()


async def delete_city(city: int, db: AsyncSession) -> Response:
    city = await get_city_by_id_or_404(city, db)
    await db.delete(city)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
