from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models, schemas


async def get_city_by_name(db: AsyncSession, city_name: str):
    selection = select(models.City).where(models.City.name == city_name)
    result = await db.execute(selection)
    return result.scalars().first()


async def get_city_by_id(db: AsyncSession, cid: int) -> models.City:
    selection = select(models.City).where(models.City.id == cid)
    res = await db.execute(selection)
    return res.scalars().first()


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    selection = select(models.City)
    res = await db.execute(selection)
    return res.scalars().all()


async def get_all_cities_dict(db: AsyncSession) -> list[dict[str, str | int]]:
    cities = await get_all_cities(db)
    return [{"name": city.name, "id": city.id} for city in cities]


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    created = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(created)
    await db.commit()
    await db.refresh(created)
    return created


async def delete_city(db: AsyncSession, city: models.City) -> None:
    await db.delete(city)
    await db.commit()
    return


async def update_city(
    db: AsyncSession, city_id: int, city_data: schemas.CityCreate
) -> models.City:
    city = await get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    for key, value in city_data.model_dump().items():
        setattr(city, key, value)
    await db.commit()
    await db.refresh(city)
    return city
