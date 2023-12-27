from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models
from . import schemas


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_all_city(db: AsyncSession):
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await db.execute(select(models.City)
                               .filter(models.City.id == city_id))
    db_city = db_city.scalar()

    if db_city:
        await db.delete(db_city)
        await db.commit()

        return "City deleted successfully"
