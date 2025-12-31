from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import Union

from city_crud_api.models import DBCity
from dependencies import get_db, get_async_db, DbAsyncDep, DbSyncDep, CityIdQuery
from temperature_api import crud
from temperature_api.crud import  add_temperature_to_db
from temperature_api.schemas import Temperature, TemperatureValue

import asyncio
import httpx

router = APIRouter()


@router.get("/temperatures/", tags=["temperatures"], response_model=Union[list[Temperature], list[TemperatureValue]])
def read_temperatures(db: DbSyncDep, city_id: CityIdQuery):
    if city_id:
        city_temperature_list = crud.get_city_temperatures(city_id=city_id, db=db)

        return [
            TemperatureValue(
                temperature=city_temperature[0],
                date_time=city_temperature[1]
            )
            for city_temperature in city_temperature_list
        ]
    return crud.get_temperatures(db=db)


@router.post("/temperatures/update", tags=["temperatures"])
async def update_temperatures(db_async: DbAsyncDep):
    cities_id_name = await db_async.execute(select(DBCity.id, DBCity.name))
    result_cities_id_name = cities_id_name.all()
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            [tg.create_task(add_temperature_to_db(id=id, name=name, db_async=db_async, client=client)) for id, name in result_cities_id_name]
        await db_async.commit()
        return {"Updated": True}
