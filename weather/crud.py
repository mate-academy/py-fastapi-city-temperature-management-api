from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import City, Temperature
from schemas import CityCreate


# ------------------------ City ------------------
async def get_all_city_crud(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()


async def create_city_crud(db: AsyncSession, city: CityCreate):
    db_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city_by_id_crud(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    return result.scalars().first()


async def update_city_crud(db: AsyncSession,
                           city_id: int, city_data: CityCreate):
    city = await get_city_by_id_crud(db, city_id)
    if not city:
        return None
    city.name = city_data.name
    city.additional_info = city_data.additional_info
    await db.commit()
    await db.refresh(city)
    return city


async def city_delete_crud(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()
    if city:
        await db.delete(city)
        await db.commit()
        return True
    return False


# ---------------------- Temperature ----------------------------
async def get_all_city_names_crud(db: AsyncSession):
    result = await db.execute(select(City.name))
    return [row[0] for row in result.all()]


async def update_temperature_cities_crud(db: AsyncSession,
                                         city_name: str, temperature: float):
    result = await db.execute(select(City).where(City.name == city_name))
    city = result.scalars().first()
    if city:
        temp_record = Temperature(city_id=city.id, temperature=temperature)
        db.add(temp_record)
        await db.commit()
        await db.refresh(temp_record)
        return temp_record
    return None


async def get_all_temperaturs_crud(db: AsyncSession):
    result = await db.execute(select(Temperature))
    return result.scalars().all()


async def get_temparature_by_city_id_crud(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(Temperature).where(Temperature.city_id == city_id)
        )
    return result.scalars().all()
