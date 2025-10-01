from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from src.city.models import DbCity
from src.city.schemas import CityCreate, CityUpdate, CityRead


def get_all_city_selection() -> Select:
    return select(DbCity)

def filter_by_city_id(selection: Select, city_id: int | None) -> Select:
    if city_id is not None:
        selection = selection.where(DbCity.id == city_id)
    return selection

def filter_by_city_name(selection: Select, city_name: str) -> Select:
    return selection.where(DbCity.name == city_name)

async def read_city_by_city_name(db: AsyncSession, city_name: str) -> DbCity:
    selection = get_all_city_selection()
    selection = filter_by_city_id(selection, city_name)
    result = await db.execute(selection)
    return result.scalar_one_or_none()

async def create_city(db: AsyncSession, city_data: CityCreate) -> DbCity:
    city_in_db = await read_city_by_city_name(db=db, city_name=city_data.name)
    if city_in_db is not None:
        city = DbCity(**city_data.model_dump())
        db.add(city)
        await db.commit()
        await db.refresh(city)
        return city
    raise HTTPException(status_code=400, detail=f"City with this name '{city_data.name}' already exists")

async def read_all_cities(db: AsyncSession) -> list[CityRead]:
    stmt = get_all_city_selection()
    result = await db.execute(stmt)
    cities = result.scalars().all()
    return [CityRead.model_validate(city) for city in cities]


async def read_city_by_id(db: AsyncSession, city_id: int) -> DbCity:
    selection = get_all_city_selection()
    selection = filter_by_city_id(selection, city_id)
    result = await db.execute(selection)
    city = result.scalars().first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

async def put_city_by_id(
        db: AsyncSession, city_id: int, data: CityUpdate
) -> DbCity:
    city = await read_city_by_id(db, city_id)
    updates = data.model_dump()
    for key, value in updates.items():
        setattr(city, key, value)
    await db.commit()
    await db.refresh(city)
    return city
