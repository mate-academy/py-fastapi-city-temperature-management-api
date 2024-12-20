from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from City_CRUD_API import models
from City_CRUD_API.schemas import CityCreate


async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    return result.scalars().first()


async def get_city_by_name(db: AsyncSession, name: str):
    """
    In case the same city already exists
    """
    result = await db.execute(
        select(models.City).filter(models.City.name == name)
    )
    return result.scalars().first()


async def update_city(
        db: AsyncSession,
        city_id: int,
        name: str = None,
        additional_info: str = None,
):
    city = await get_city_by_id(db, city_id)
    if not city:
        return None

    if name:
        city.name = name
    if additional_info:
        city.additional_info = additional_info

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db, city_id)
    if not city:
        return {"detail": f"City with ID {city_id} not found."}

    await db.delete(city)
    await db.commit()

    return {"detail": f"City with ID {city_id} deleted successfully."}
