from fastapi import status
from fastapi.responses import HTMLResponse
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.cities.models import DBCity
from src.cities.schemas import CityCreate, CRUDDetails


async def get_all_cities(db: AsyncSession) -> list[DBCity]:
    query = select(DBCity)
    city_list = await db.execute(query)
    return city_list.scalars()


async def create_new_city(db: AsyncSession, city: CityCreate) -> CRUDDetails:
    query = insert(DBCity).values(**city.model_dump())
    try:
        result = await db.execute(query)
    except IntegrityError as ie:
        return HTMLResponse(
            content=CRUDDetails(
                id=None, message=ie._message(), status="failure"
            ).model_dump_json(),
            status_code=status.HTTP_409_CONFLICT,
        )
    await db.commit()
    return CRUDDetails(id=result.lastrowid, status="success")


async def delete_city_by_id(db: AsyncSession, city_id: int) -> CRUDDetails:
    query = delete(DBCity).where(DBCity.id == city_id)
    result = await db.execute(query)
    success = bool(result.rowcount)
    await db.commit()
    return CRUDDetails(
        id=city_id, status="success" if success else "does_not_exist"
    )
