from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert, update, delete

from cities import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_city_by_id(city_id: int, db: AsyncSession):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)

    try:
        city = result.scalar_one()

    except NoResultFound:
        return None

    return city


async def create_city(db: AsyncSession, city: schemas.CityCreateSchema):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdateSchema):
    existing_city = await get_city_by_id(city_id=city_id, db=db)

    if existing_city is None:
        return None

    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(
            name=city.name,
            additional_info=city.additional_info
        )
        .returning(models.City.id)
    )
    result = await db.execute(query)

    await db.commit()

    updated_id = result.scalar_one_or_none()

    resp = {**city.model_dump(), "id": result.inserted_primary_key[0]}

    return resp


async def delete_city(db: AsyncSession, city_id: int):
    existing_city = await get_city_by_id(db=db, city_id=city_id)

    if existing_city is None:
        return None

    query = delete(models.City).where(models.City.id == city_id)

    await db.execute(query)

    await db.commit()

    return {"message": f"City with id {city_id} has been deleted."}