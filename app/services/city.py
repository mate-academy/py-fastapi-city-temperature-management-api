from sqlalchemy import select

from app.models.city import CityModel
from app.database.config import AsyncDatabaseSession
from app.schemas.city import CityCreateSchema, CityUpdateSchema


async def retrieve_city(
    db: AsyncDatabaseSession, city_id: int
) -> CityModel | None:
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.scalars(stmt)
    return result.first()


async def retrieve_city_by_name(
    db: AsyncDatabaseSession, city_name: str
) -> CityModel | None:
    stmt = select(CityModel).where(CityModel.name == city_name)
    result = await db.scalars(stmt)
    return result.first()


async def list_cities(db: AsyncDatabaseSession) -> list[CityModel]:
    stmt = select(CityModel)
    result = await db.scalars(stmt)
    return result.all()


async def create_city(
    db: AsyncDatabaseSession, city: CityCreateSchema
) -> CityModel:
    new_city = CityModel(**city.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def update_city(
    db: AsyncDatabaseSession, city_id: int, city: CityUpdateSchema
) -> CityModel:
    db_city = await retrieve_city(db=db, city_id=city_id)
    update_data = city.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_city, key, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncDatabaseSession, city_id: int) -> None:
    city = await retrieve_city(db=db, city_id=city_id)
    if city:
        await db.delete(city)
        await db.commit()
