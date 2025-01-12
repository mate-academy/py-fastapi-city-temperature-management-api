from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    a = [city[0] for city in cities_list.fetchall()]
    return a


async def create_city(db: AsyncSession, city: schemas.CreateCity):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.dict(), "id": result.inserted_primary_key}
    return resp


async def update_city(db: AsyncSession, city_id: int, city: schemas.UpdateCity):
    # Query to find the existing city
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    selected_city = result.scalar_one_or_none()

    if selected_city is None:
        # Handle case where city is not found
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    # Perform the update with non-null values from the request
    update_query = update(models.City).where(models.City.id == city_id).values(
        **{key: value for key, value in city.dict(exclude_unset=True).items() if value is not None}
    )
    await db.execute(update_query)
    await db.commit()

    # Reload the updated city to reflect the changes
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    updated_city = result.scalar_one()

    return [updated_city]  # Returning a list of cities (as required by your response model)


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.City).where(models.City.id == city_id)
    await db.execute(query)
    await db.commit()
    return {"deleted_city": f"City with id {city_id} deleted"}


async def get_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    b = result.fetchone()
    if b is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")
    return [b[0]]
