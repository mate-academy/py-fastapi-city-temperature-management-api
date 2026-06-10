from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def create_city(
    db: AsyncSession,
    city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        name = city.name,
        additional_info = city.additional_info.model_dump()
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(
    db: AsyncSession,
    city_id: int
) -> models.City | None:
    
    return await db.scalar(
        select(models.City)
        .where(models.City.id == city_id)
    )


async def get_cities(
    db: AsyncSession,
    skip: int | None = None,
    limit: int | None = None
) -> list[models.City]:
    
    query = select(models.City)

    if skip is not None:
        query = query.offset(skip)

    if limit is not None:
        query = query.limit(limit)

    cities = await db.scalars(query)
    return cities.all()


async def delete_city_by_id(
    db: AsyncSession,
    city_id: int
) -> models.City | None:
    city = await get_city_by_id(city_id=city_id, db=db)
    
    if city is not None:
        await db.delete(city)
        await db.commit()
        return city
    return None


async def update_city_by_id(
    db: AsyncSession,
    city_id: int,
    city_data: schemas.CityCreate
) -> models.City | None:
    city = await get_city_by_id(city_id=city_id, db=db)
    
    if city is not None:
        city.name = city_data.name
        city.additional_info = city_data.additional_info.model_dump()
        await db.commit()
        await db.refresh(city)
        return city
    
    return None