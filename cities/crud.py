from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession


from cities import models, schemas
from cities.models import DBCity


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).filter(models.DBCity.id == city_id)
    result = await db.execute(query)
    db_city = result.scalar_one_or_none()
    return db_city


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {
        **city.model_dump(),
        "id": result.lastrowid
    }
    return response


async def update_city_info(
        db: AsyncSession,
        city: schemas.CityUpdate,
        city_id: int
):
    query = select(models.DBCity).filter(DBCity.id == city_id)
    result = await db.execute(query)
    db_city = result.scalar_one_or_none()

    if city.additional_info:
        db_city.additional_info = city.additional_info

    if city.name:
        db_city.name = city.name

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.DBCity).where(
        models.DBCity.id == city_id
    ).returning(models.DBCity.name)
    result = await db.execute(query)
    city_name = result.scalar_one_or_none()
    await db.commit()

    if city_name:
        return {"message": f"City {city_name} deleted successfully"}
