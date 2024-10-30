from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from cities import schemas, models


async def create_city(
    db: AsyncSession, city: schemas.CityCreate
) -> schemas.City:
    city_data = city.model_dump()
    query = insert(models.City).values(city_data).returning(models.City.id)
    result = await db.execute(query)
    await db.commit()
    city_id = result.scalar()
    return schemas.City(id=city_id, **city_data)


async def get_city_by_id(
        db: AsyncSession, city_id: int
) -> Optional[models.City]:
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    return result.scalar()


async def update_city_info(
    db: AsyncSession, city_id: int, update_data: schemas.CityUpdate
) -> Optional[models.City]:
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalar()

    if city is None:
        return None

    update_data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city: models.City) -> str:
    success_message = f'The city "{city.name}" has been deleted'
    await db.delete(city)
    await db.commit()
    return success_message


async def get_all_cities(db: AsyncSession) -> list[schemas.City]:
    query = select(models.City)
    result = await db.execute(query)
    cities = result.scalars().all()
    return [schemas.City(**city.__dict__) for city in cities]


async def create_temperatures(db: AsyncSession, new_data: list[dict]):
    query = insert(models.Temperature).values(new_data)
    await db.execute(query)
    await db.commit()
    return "Temperatures for all cities have been updated"


async def get_all_temperatures(db: AsyncSession) -> list[schemas.Temperature]:
    query = select(
        models.Temperature
    ).options(
        joinedload(models.Temperature.city)
    )
    result = await db.execute(query)
    temperatures = result.scalars().all()
    return [
        schemas.Temperature(**temperature.__dict__)
        for temperature in temperatures
    ]


async def get_city_temperatures(
    db: AsyncSession, city_id: int
) -> list[schemas.Temperature]:
    query = (
        select(models.Temperature)
        .options(joinedload(models.Temperature.city))
        .where(models.Temperature.city_id == city_id)
    )
    result = await db.execute(query)
    temperatures = result.scalars().all()
    return [
        schemas.Temperature(**temperature.__dict__)
        for temperature in temperatures
    ]
