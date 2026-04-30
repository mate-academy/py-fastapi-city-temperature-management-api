from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from db.dependencies import get_session
from db.exc import DatabaseError
from temperature.dependencies import get_client
from city.crud import aget_cities_list
from temperature import schemas, crud, services

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("", response_model=list[schemas.Temperature])
async def read_temperatures(
    asession: Annotated[AsyncSession, Depends(get_session)],
    city_id: Annotated[int | None, Query()] = None,
) -> Any:
    return list(await crud.aget_temperatures_list(asession, city_id))


@router.post("/update")
async def create_temperature_data(
    asession: Annotated[AsyncSession, Depends(get_session)],
    aclient: Annotated[AsyncClient, Depends(get_client)],
):
    cities_list = await aget_cities_list(asession)
    cities_list = list(cities_list.all())
    data = await services.fetch_temperature_data(aclient, cities_list)
    try:
        await crud.acreate_temperatures(asession, data)
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.message)
    return Response(status_code=200)
