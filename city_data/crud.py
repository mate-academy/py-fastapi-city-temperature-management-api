from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models


async def get_all_cities(db: AsyncSession,
                         skip: int = 0,
                         limit: int = 10) -> list | None:
    query = select(models.DBCity).offset(skip).limit(limit)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.all()]


async def get_city_by_name(
        db: AsyncSession, name: str
) -> models.DBCity | None:
    query = select(models.DBCity).where(
        models.DBCity.name == name.capitalize()
    )
    city = await db.execute(query)
    return city.scalar()


async def get_city_by_id(
        db: AsyncSession, city_id: int
) -> models.DBCity | None:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def get_city_by_name_exclude_id(
        db: AsyncSession,
        city_name: str, city_id: int
) -> models.DBCity | None:
    query = select(models.DBCity).where(
        models.DBCity.id != city_id,
        models.DBCity.name == city_name.capitalize()
    )
    city = await db.execute(query)
    return city.scalar()


async def create_city(
        db: AsyncSession, city: schemas.CityCreate
) -> dict:
    query = insert(models.DBCity).values(
        name=city.name.capitalize(),
        additional_info=city.additional_info,
    )
    created_city = await db.execute(query)
    await db.commit()
    return {**city.dict(), "id": created_city.lastrowid}
    # return {**city.model_dump(), "id": created_city.lastrowid}


async def delete_city(
        db: AsyncSession, city_id: int
) -> dict | None:
    query = delete(models.DBCity).where(models.DBCity.id == city_id)
    del_city = await db.execute(query)
    if del_city.rowcount == 0:
        return None
    await db.commit()
    return {"message": f"Successfully deleted (id: {city_id})"}


async def delete_all_cities(db: AsyncSession) -> dict | None:
    query = delete(models.DBCity)
    del_cities = await db.execute(query)
    if del_cities.rowcount == 0:
        return None
    await db.commit()
    return {"message": f"Successfully deleted {del_cities.rowcount} city(ies)"}


async def update_city_info(
        db: AsyncSession,
        city: schemas.CityBase, city_id: int
) -> dict:
    query = update(models.DBCity).where(
        models.DBCity.id == city_id
    ).values(
        name=city.name.capitalize(),
        additional_info=city.additional_info
    )
    await db.execute(query)
    await db.commit()
    return {**city.dict(), "message": "Update successful"}
