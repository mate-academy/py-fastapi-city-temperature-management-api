from typing import Sequence

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_cities_list(db: AsyncSession) -> Sequence[models.City]:
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
    query = select(models.City).filter(models.City.name == name)
    result = await db.execute(query)
    return result.scalars().first()


async def get_city_by_id_or_404(
        db: AsyncSession,
        city_id: int
) -> models.City:
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    db_city = result.scalars().first()

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    if await get_city_by_name(db, city.name):
        raise HTTPException(
            status_code=400,
            detail=f"City '{city.name}' already exists"
        )

    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_data: schemas.CityUpdate
) -> models.City:
    existed_city = await get_city_by_name(db, city_data.dict()["name"])

    if existed_city and existed_city.id != city_id:
        raise HTTPException(
            status_code=400,
            detail=f"City '{existed_city.name}' already exists"
        )

    db_city = await get_city_by_id_or_404(db, city_id)

    for attr, value in city_data.dict().items():
        setattr(db_city, attr, value)

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> Response:
    db_city = await get_city_by_id_or_404(db, city_id)
    await db.delete(db_city)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
