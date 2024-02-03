from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from dependencies import CommonsDep


async def get_all_cities(
    db: AsyncSession, commons: CommonsDep | None
) -> list[models.CityDB]:
    query = select(models.CityDB)
    if commons:
        if "q" in commons and commons["q"]:
            query = query.filter(models.CityDB.name.ilike(f"%{commons['q']}%"))
        query = query.offset(commons.get("skip", 0)).limit(commons.get("limit", 100))
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict[str, None]:
    query = insert(models.CityDB).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.CityDB:
    query = select(models.CityDB).filter(models.CityDB.id == city_id)
    result = await db.execute(query)

    city = result.scalar_one_or_none()

    return city


async def update_city(
    db: AsyncSession, city_id: int, updated_city: schemas.CityUpdate
) -> models.CityDB:
    query = select(models.CityDB).filter(models.CityDB.id == city_id)
    result = await db.execute(query)

    city = result.scalar_one_or_none()

    if city:
        for key, value in updated_city.model_dump().items():
            if hasattr(city, key):
                setattr(city, key, value)
        await db.commit()
        await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.CityDB).filter(models.CityDB.id == city_id)
    result = await db.execute(query)

    city = result.scalar_one_or_none()

    if city:
        await db.delete(city)
        await db.commit()

    return city
