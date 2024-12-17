from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()

    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_city_by_name_additional_info(
        db: AsyncSession,
        city_name: str,
        city_additional_info: str
):
    query = select(models.DBCity).where((models.DBCity.name == city_name) &
                                        (models.DBCity.additional_info ==
                                         city_additional_info))
    result = await db.execute(query)
    return result.scalars().first()


async def get_cities(db: AsyncSession, skip: int = 0, limit: int | None = 10):
    query = await db.execute(
        select(models.DBCity).offset(skip).limit(limit)
    )
    return query.scalars().all()


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdate):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    db_city = result.scalars().first()

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, db_city: models.DBCity):
    await db.delete(db_city)
    await db.commit()

    return {"message": "City successfully deleted"}
