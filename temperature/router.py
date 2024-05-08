from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

from engine import session_manager
import city.models
import city.crud
from temperature import crud, schemas

router = APIRouter()


@router.post(path="/temperature/{city}/update",
             tags=["Temperatures"])
async def add_specific_city_temp_record(
        city_name: str,
        session: AsyncSession = Depends(session_manager)):
    query = (select(city.models.DBCity.country).
             where(city.models.DBCity.name == city_name))

    country_name = await session.execute(query)

    return await crud.create_new_temp_record(
        session=session,
        city_name=city_name,
        country=country_name.scalar_one())


@router.post("/temperature/update_all",
             tags=["Temperatures"])
async def add_temp_records_for_all_cities(
        session: AsyncSession = Depends(session_manager)):
    """
    :param session: this function uses asynchronous loop
    """
    get_city_list = await city.crud.get_all_cities(session=session,
                                                   skip=0,
                                                   limit=99999)
    tasks = []
    city_names_list = []
    for city_obj in get_city_list:
        city_names_list.append(city_obj.name)
        tasks.append(crud.create_new_temp_record(
            session=session,
            city_name=city_obj.name,
            country=city_obj.country
        ))
    await asyncio.gather(*tasks)

    return (f"Current temperature values for the following cities:"
            f"{', '.join(city_names_list)}, were successfully "
            f"added to the Database")


@router.get(path="/temperature/",
            response_model=list[schemas.TemperatureBase],
            tags=["Temperatures"])
async def read_all_temperature_records(
        session: AsyncSession = Depends(session_manager),
        skip: int = 0,
        limit: int = 10):
    get_temp_list = await crud.get_all_records(
        session=session,
        skip=skip,
        limit=limit)
    if not get_temp_list:
        raise HTTPException(status_code=404,
                            detail="No records found")
    return get_temp_list


@router.get(path="/temperature/{city_name}",
            response_model=list[schemas.TemperatureBase],
            tags=["Temperatures"])
async def read_specific_city_records(
        city_name: str,
        session: AsyncSession = Depends(session_manager),
        skip: int = 0,
        limit: int = 10):
    check_records = await crud.get_city_records(
        session=session,
        city_name=city_name,
        skip=skip,
        limit=limit
    )
    if len(check_records) == 0:
        raise HTTPException(status_code=404,
                            detail="No records found")
    return check_records
