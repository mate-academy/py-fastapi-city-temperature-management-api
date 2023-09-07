from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models
from city import schemas


async def get_all_cities(data_base: AsyncSession, skip: int, limit: int) -> list:
    queryset = select(models.DBCity).offset(skip).limit(limit)
    cities = await data_base.execute(queryset)

    return [city for city in cities.scalars()]


async def create_city(data_base: AsyncSession, city: schemas.CityCreate):
    new_city = models.DBCity(**city.model_dump())
    data_base.add(new_city)
    await data_base.commit()
    await data_base.refresh(new_city)
    return new_city


async def check_city_by_name(data_base: AsyncSession, name: str) -> bool:
    query = select(models.DBCity).where(models.DBCity.name == name)
    city = await data_base.execute(query)
    city = city.fetchone()
    if city:
        return True

    return False


async def update_city(data_base: AsyncSession, city_id: int, data: dict) -> None | models.DBCity:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    new_city = await data_base.execute(query)
    new_city = new_city.fetchone()

    if new_city:
        new_city = new_city[0]

        for key, value in data.items():
            setattr(new_city, key, value)

        await data_base.commit()
        await data_base.refresh(new_city)

        return new_city

    return None


async def get_city_by_id(data_base: AsyncSession, city_id: int) -> schemas.City | None:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    city = await data_base.execute(query)
    city = city.fetchone()
    if city:
        return city[0]
    return None


async def delete_city(data_base: AsyncSession, city_id: int) -> bool:
    city = await data_base.get(models.DBCity, city_id)
    if city:
        await data_base.delete(city)
        await data_base.commit()
        return True
    return False



