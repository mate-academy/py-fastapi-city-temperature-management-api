from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from city import schemas, models


async def create_new_city(session: AsyncSession,
                          city: schemas.CityBase):
    query = insert(models.DBCity).values(
        name=city.name,
        country=city.country,
        additional_info=city.additional_info
    )
    result = await session.execute(query)
    await session.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def get_all_cities(session: AsyncSession,
                         skip: int = 0,
                         limit: int = 10):
    query = (select(models.DBCity).
             offset(skip).limit(limit))
    city_data = await session.execute(query)
    return [city[0] for city in city_data.all()]


async def get_city_by_name(session: AsyncSession,
                           city_name: str):
    query = (select(models.DBCity).
             where(models.DBCity.name == city_name))
    city_result = await session.execute(query)
    return city_result.scalar()


async def update_city_info(session: AsyncSession,
                           city: schemas.CityBase,
                           city_name: str):
    query = (update(models.DBCity).
             where(models.DBCity.name == city_name).
             values(name=city.name,
                    country=city.country,
                    additional_info=city.additional_info))
    await session.execute(query)
    await session.commit()
    return {"message": f"city details for city "
                       f"'{city_name}' were amended"}


async def delete_city(session: AsyncSession,
                      city_name: str):
    delete_query = (delete(models.DBCity).
                    where(models.DBCity.name == city_name))
    await session.execute(delete_query)
    await session.commit()
    return {"message": f"city with name '{city_name}' "
                       f"was deleted from the Database"}
