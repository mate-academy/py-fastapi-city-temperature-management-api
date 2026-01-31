import httpx

import datetime

from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from models import get_session, DBTemperature, DBCity, get_async_session

from temperature_api.schemas import (
    TemperatureRead,
    TemperatureUpdate
)

from .additional_funcs_for_api import get_geocoded_city, get_temperatures


SessionDep = Annotated[Session, Depends(get_session)]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(session: AsyncSessionDep):
    result = await session.scalars(select(DBCity))
    cities = result.all()

    async with httpx.AsyncClient(timeout=10) as client:
        for city in cities:
            try:
                coordinates = await get_geocoded_city(city.name, client)
                temp = await get_temperatures(coordinates, client)

                obj = DBTemperature(
                    city_id=city.id,
                    date_time=datetime.datetime.now(datetime.UTC),
                    temperature=temp,
                )
                session.add(obj)

            except Exception as e:
                # logs
                print(f"Failed for city {city.name}: {e}")

    await session.commit()

    return {"success": True}


@router.get("/temperatures", response_model=List[TemperatureRead])
async def list_temperatures(
        city_id: Optional[int] = Query(None, description="Filter temperatures by city ID"),
        session: AsyncSessionDep = Depends(get_async_session)
):
    stmt = select(DBTemperature)

    if city_id is not None:
        stmt = stmt.where(DBTemperature.city_id == city_id)

    result = await session.scalars(stmt)
    return result.all()
