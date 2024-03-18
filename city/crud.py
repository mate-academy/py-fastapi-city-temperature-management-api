from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


from dependencies import update_db_object
from . import schemas
from .models import DBCity


async def get_all_cities(db: AsyncSession):
    query = select(DBCity)
    cities = await db.execute(query)
    return [city[0] for city in cities]


async def create_city(
        db: AsyncSession, city: schemas.CreateCity
) -> dict:
    query = insert(DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )

    result = await db.execute(query)
    await db.commit()

    return {**city.model_dump(), "id": result.lastrowid}


async def get_city(db: AsyncSession, city_id: int) -> DBCity | None:
    query = select(DBCity).where(DBCity.id == city_id)
    city = await db.execute(query)
    return city.scalars().first()


async def update_city(
        db: AsyncSession, city_id: int, city: schemas.UpdateCity
) -> schemas.City | None:

    db_city = await get_city(db=db, city_id=city_id)

    if db_city:
        db_city = await update_db_object(
            db=db, current_object=db_city, new_object=city
        )
        return schemas.City.from_orm(db_city)


async def delete_city(db: AsyncSession, city_id: int) -> DBCity | None:
    db_city = await get_city(db=db, city_id=city_id)

    if db_city:
        await db.delete(db_city)
        await db.commit()
        return db_city
