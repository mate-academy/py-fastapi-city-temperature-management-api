from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from city.models import City


async def get_all_cities(db: AsyncSession):
    query = select(City)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(City).where(City.id == city_id)
    city = await db.execute(query)

    if not city.scalar():
        raise HTTPException(
            status_code=404,
            detail=f"The city with id {city_id} does not exist",
        )
    else:
        return city.scalar()


async def create_city(db: AsyncSession, city_data: schemas.CityCreate):
    query = insert(City).values(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city_data.model_dump(), "id": result.lastrowid}
    return response


async def update_city(
    db: AsyncSession, city_data: schemas.CityCreate, city_id: int
):
    city_to_update = await get_city_by_id(db, city_id=city_id)

    if city_to_update:
        for key, value in city_data.dict().items():
            setattr(city_to_update, key, value)
        async with db.begin():
            await db.commit()
            await db.refresh(city_to_update)

    return city_to_update


async def delete_city(db: AsyncSession, city_id: int):
    city_to_delete = await get_city_by_id(db, city_id=city_id)

    if city_to_delete:
        async with db.begin():
            await db.delete(city_to_delete)
            await db.commit()
        return True
    else:
        return False
