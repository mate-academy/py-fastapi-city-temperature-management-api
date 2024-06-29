import asyncio

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependences import DB_DEPENDENCY
from temperature import crud
from temperature import schemas

router = APIRouter()


@router.post("/temperatures/update/", status_code=201)
async def update_temperatures_of_all_cities(db: AsyncSession = DB_DEPENDENCY):
    await asyncio.create_task(crud.update_temperatures(db))


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_list_temperatures(city_id: int | None = None, db: AsyncSession = DB_DEPENDENCY):
    return await crud.get_list_temperatures(db, city_id)
