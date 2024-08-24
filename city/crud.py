from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

import city
from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city_to_delete = result.scalar_one_or_none()

    if city_to_delete is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    delete_query = delete(models.City).where(models.City.id == city_id)
    await db.execute(delete_query)
    await db.commit()

    return {"status": "success", "message": f"City with id {city_id} deleted"}
